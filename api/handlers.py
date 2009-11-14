import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers

from piston.handler import BaseHandler
from piston.authentication import HttpBasicAuthentication
from piston.utils import rc

from stark.apps.world.models import Room, RoomConnector
from stark.apps.anima.models import Player, Mob, Message

ROOM_RANGE = 10

class RoomHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Room
    fields = ('id', 'title', 'description', 'xpos', 'ypos', 'type', 'north', 'east', 'south', 'west',
              ('player_related', ('id', 'name')),
              ('mob_related', ('id', 'name'))
              )

    
    def update(self, request, *args, **kwargs):
        try:
            # only a builder can change a room
            if not Player.objects.get(user=request.user, status='logged_in').builder_mode:
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
                        connector.direction = k
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
        player = Player.objects.get(user=request.user, status='logged_in')
        room = Room.objects.get(pk=id)
        
        if player.room == room:
            # if possible, move the player to an adjacent room, otherwise to
            # the origin
            adjacent_rooms = room.from_room.all()
            if adjacent_rooms:
                player.room = adjacent_rooms[0].to_room
            else:
                player.room = Room.objects.get(pk=1)
            player.save()
            
        room.delete()
        
        return rc.DELETED


    @classmethod
    def __determine_connection(self, room, direction):
        try:
            return room.from_room.get(direction=direction).type
        except RoomConnector.DoesNotExist:
            return None
        
        try:
            to_room = Room.objects.get(xpos=room.xpos + delta['x'], ypos = room.ypos + delta['y'])
            try:
                return RoomConnector.objects.get(from_room=room, to_room=to_room).type
            except RoomConnector.DoesNotExist:
                return None
        except Room.DoesNotExist:
            return None

    @classmethod
    def north(self, room): return self.__determine_connection(room, 'north')
    
    @classmethod
    def east(self, room): return self.__determine_connection(room, 'east')

    @classmethod
    def south(self, room): return self.__determine_connection(room, 'south')

    @classmethod
    def west(self, room): return self.__determine_connection(room, 'west')

class MapHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        if request.user.is_authenticated():
            player = Player.objects.get(user=request.user, status='logged_in')
            rooms = []
            min_x = None
            min_y = None
            
            for room in Room.objects.filter(
                            xpos__gt=player.room.xpos - ROOM_RANGE,
                            xpos__lt=player.room.xpos + ROOM_RANGE,
                            ypos__gt=player.room.ypos - ROOM_RANGE,
                            ypos__lt=player.room.ypos + ROOM_RANGE):
                
                # keep track of the lowest x
                if not min_x: min_x = room.xpos
                elif room.xpos < min_x: min_x = room.xpos
                
                # keep track of the lowest y
                if not min_y: min_y = room.ypos
                elif room.ypos < min_y: min_y = room.ypos
                
                # Because django-piston automatically looks up objects if
                # they've been previously defined as a handler's model (which
                # is the case for Room), I specifically fetch the room
                # attributes I need to speed up this api call.
                # If you let piston do this for you it's 5 to 10 times slower
                room_dict = {
                    'xpos': room.xpos,
                    'ypos': room.ypos,
                    'type': room.type,
                }
                
                for connection in room.from_room.all():
                    room_dict[connection.direction] = connection.type
                
                rooms.append(room_dict)

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
            player = Player.objects.get(user=request.user, status='logged_in')
        else:
            player = Player.objects.get(pk=id) # TODO: this should probably return some kind of error instead
        return player
    
    def update(self, request, id=None):
        try:# TODO: remove this eventually

            player = Player.objects.get(user=request.user, status='logged_in')

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
                                                to_room.type = 'field'
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

class MessageHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')
    model = Message
    fields = ('content', 'type', 'created', 'source')
    
    def read(self, request, *args, **kwargs):
        return Message.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            content = request.POST['content']
            type = request.POST['type']
            message = Message.objects.create(
                created=datetime.datetime.now(),
                type=type,
                content=content,
                author=Player.objects.get(user=request.user, status='logged_in'),
            )
            return message
        except Exception, e:
            print u"exception: %s" % e
            return rc.BAD_REQUEST
    
    @classmethod
    def source(self, message):
        return u"%s" % message.author.name

class PingHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    def read(self, request):
        return {'status': 'OK'}