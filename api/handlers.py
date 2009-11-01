from django.contrib.auth.decorators import login_required
from django.core import serializers

from piston.handler import BaseHandler
from piston.authentication import HttpBasicAuthentication
from piston.utils import rc

from stark.apps.world.models import Room, RoomConnector
from stark.apps.anima.models import Player, Mob

RANGE = 10


class RoomHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = Room
    fields = ('id', 'title', 'description', 'xpos', 'ypos', 'north', 'east', 'south', 'west')
    
    def update(self, request, *args, **kwargs):
        try:
            if not Player.objects.get(user=request.user).builder_mode:
                return rc.FORBIDDEN
            super(RoomHandler, self).update(request, *args, **kwargs)
            return Room.objects.get(id=kwargs['id'])
        except Exception:
            return rc.BAD_REQUEST

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
    model = Room
    fields = ('id', 'title', 'description', 'xpos', 'ypos', 'north', 'east', 'south', 'west')

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
    


    

class PlayerHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT')
    model = Player
    fields = (
        'id',
        'name',
        'level',
        'builder_mode',
        ('room', (
            'id',
            'title',
            'description',
            'xpos',
            'ypos',
            ('player_related', (
                'id', 'name'),),
            ('mob_related', (
                'id', 'name'),)
            ),
        ),
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
                    # if we haven't errored out, then there exists a connection to those coordinates
                    player.room = connector.to_room
                    player.save()
                except RoomConnector.DoesNotExist:
                    #return rc.BAD_REQUEST # uncomment to enable staff god mode
                    # Admins can create new connections or new rooms by
                    # walking around
                    if player.builder_mode:
                        try:
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if abs(i) != abs(j):
                                        if player.room.xpos + i == x and player.room.ypos + j == y:
                                            to_room, is_new = Room.objects.get_or_create(xpos=x, ypos=y)
                                            if is_new:
                                                to_room.title = 'Untitled room'
                                                to_room.save()
                                            connector = RoomConnector(from_room=player.room, to_room=to_room)
                                            connector.type = 'Normal'
                                            connector.save()
                                            player.room = to_room
                                            player.save()
                                            return player
                        except Room.DoesNotExist:
                            return rc.BAD_REQUEST
                    else:
                        return rc.BAD_REQUEST

            if request.PUT.has_key('builder_mode'):
                if player.level < 100:
                    return rc.BAD_REQUEST
                
                if request.PUT['builder_mode'] in (u'false', None):
                    player.builder_mode = False;
                else:
                    player.builder_mode = True;
                player.save()

            return player

        except Exception, e:
            print "exception: %s" % e
            raise Exception
