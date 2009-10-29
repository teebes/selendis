from django.contrib.auth.decorators import login_required
from django.core import serializers

from piston.handler import BaseHandler
from piston.authentication import HttpBasicAuthentication
from piston.utils import rc

from stark.apps.world.models import Room
from stark.apps.anima.models import Player, Mob

RANGE = 10

"""
fields = (
    'id', 'title', 'description', 'xpos', 'ypos',
    ('player_related', (
        'id', 'name',
    ),),
    ('mob_related', (
        'id', 'name',
    ),),)
"""

class MapHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Room
    fields = ('id', 'title', 'description', 'xpos', 'ypos')

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
        player = Player.objects.get(user=request.user)
        if request.PUT.has_key('xpos') and request.PUT.has_key('ypos'):
            x = request.PUT['xpos']
            y = request.PUT['ypos']
            from_room = player.room
            try:
                to_room = Room.objects.get(xpos=x, ypos=y)
                # TODO: validate that the client isn't returning bogus coords
                player.room = to_room
                player.save()
            except Room.DoesNotExist:
                return rc.BAD_REQUEST
        return player

class CommandHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT')
    
    def read(self, request):
        return 'hello!'
    
    def update(self, request):
        if request.PUT.has_key('command'):
            command = request.PUT['command']
            return command
        else:
            return rc.BAD_REQUEST