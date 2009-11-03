from django.contrib.auth.decorators import login_required
from django.core import serializers

from piston.handler import BaseHandler
from piston.authentication import HttpBasicAuthentication
from piston.utils import rc

from stark.apps.world.models import Room, RoomConnector
from stark.apps.anima.models import Player, Mob

RANGE = 10


class RoomHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Room
    fields = ('id', 'title', 'description', 'xpos', 'ypos', 'north', 'east', 'south', 'west',
              ('player_related', ('id', 'name')),
              ('mob_related', ('id', 'name'))
              )

    
    def update(self, request, *args, **kwargs):
        try:
            # only a builder can change a room
            if not Player.objects.get(user=request.user).builder_mode:
                return rc.FORBIDDEN
            
            from_room = Room.objects.get(pk=kwargs['id'])
            
            # if a connector has been passed, toggle accordingly, creating a
            # new empty room if need be
            for k in request.PUT.keys():
                
                def __connect_to(k):
                    if k == 'north': x, y = (0, -1)
                    elif k == 'east': x, y = (1, 0)
                    elif k == 'south': x, y = (0, 1)
                    elif k == 'west': x, y = (-1, 0)
                    to_x = from_room.xpos + x
                    to_y = from_room.ypos + y
                    
                    # if the room does not exist, 
                    
                    try:
                        to_room = Room.objects.get(xpos=to_x, ypos=to_y)
                    except Room.DoesNotExist:
                        return rc.BAD_REQUEST
                    
                    try:
                        connector = RoomConnector.objects.get(from_room=from_room, to_room=to_room)
                        connector.delete()
                    except RoomConnector.DoesNotExist:
                        connector = RoomConnector()
                        connector.from_room = from_room
                        connector.to_room = to_room
                        connector.type = 'Normal'
                        connector.save()

                if k in ('north', 'east', 'south', 'west'):
                    if request.PUT[k] == 'toggle':
                        __connect_to(k)
                        #del request.PUT[k]

            super(RoomHandler, self).update(request, *args, **kwargs)
            return Room.objects.get(id=kwargs['id'])
        except Exception, e:
            print e
            return rc.BAD_REQUEST
        
    def delete(self, request, id):
        player = Player.objects.get(user=request.user)
        room = Room.objects.get(pk=id)
        
        if player.room == room:
            player.room = Room.objects.get(pk=1)
            player.save()
            
        room.delete()
        
        return rc.DELETED

    @classmethod
    def __determine_connection(self, room, delta):
        try:
            to_room = Room.objects.get(xpos=room.xpos + delta['x'], ypos = room.ypos + delta['y'])
            try:
                return RoomConnector.objects.get(from_room=room, to_room=to_room).type
            except RoomConnector.DoesNotExist:
                return None
        except Room.DoesNotExist:
            return None

    @classmethod
    def north(self, room): return self.__determine_connection(room, {'x': 0, 'y': -1})
    
    @classmethod
    def east(self, room): return self.__determine_connection(room, {'x': 1, 'y': 0})

    @classmethod
    def south(self, room): return self.__determine_connection(room, {'x': 0, 'y': 1})

    @classmethod
    def west(self, room): return self.__determine_connection(room, {'x': -1, 'y': 0})

class MapHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        if request.user.is_authenticated():
            player, created = Player.objects.get_or_create(user=request.user, name=request.user.username)
            rooms = []
            min_x = None
            min_y = None
            for x in range(player.room.xpos - RANGE, player.room.xpos + RANGE):
                for y in range(player.room.ypos - RANGE, player.room.ypos + RANGE):
                    try:
                        rooms.append(Room.objects.get(xpos=x, ypos=y))
                        if not min_x: min_x = x
                        elif x < min_x : min_x = x
                        if not min_y: min_y = y
                        elif y < min_y: min_y = y
                    except Room.DoesNotExist: pass
        else:
            return rc.FORBIDDEN
        return {
            'starting_point': {'xpos': min_x, 'ypos': min_y},
            'player_position': {'xpos': player.room.xpos, 'ypos': player.room.ypos},
            'rooms': rooms,
        }
    

class PlayerHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT')
    model = Player
    fields = (
        'id',
        'name',
        'level',
        'builder_mode',
        'room',
    )

    def read(self, request, id=None):
        if request.user.is_authenticated():
            player, created = Player.objects.get_or_create(user=request.user, name=request.user.username)
        else:
            player = Player.objects.get(pk=id)
        return player
    
    def update(self, request, id=None):
        try:# TODO: remove this eventually

            player = Player.objects.get(user=request.user)

            if request.PUT.has_key('xpos') and request.PUT.has_key('ypos'):
                x = int(request.PUT['xpos'])
                y = int(request.PUT['ypos'])
                from_room = player.room
                try:
                    connector = RoomConnector.objects.get(from_room=from_room, to_room__xpos=x, to_room__ypos=y)
                    player.room = connector.to_room
                    player.save()
                except RoomConnector.DoesNotExist:
                    if player.builder_mode:
                        try:
                            # jump to
                            player.room = Room.objects.get(xpos=x, ypos=y)
                            player.save()
                            return player
                        except Room.DoesNotExist:
                        # Builders can create new room by walking into the
                        # non-existing space if it's adjacent to an existing
                        # room
                        # TODO: remove this, as it should be a POST call
                        # instead
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if abs(i) != abs(j):
                                        if player.room.xpos + i == x and player.room.ypos + j == y:
                                            to_room, is_new = Room.objects.get_or_create(xpos=x, ypos=y)
                                            if is_new:
                                                to_room.title = 'Untitled room'
                                                to_room.save()
                                            player.room = to_room
                                            player.save()
                                            return player
                    else:
                        return rc.BAD_REQUEST
            return player

        except Exception, e:
            print "exception: %s" % e
            raise Exception
