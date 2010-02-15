import datetime
import logging

from piston.handler import BaseHandler
from piston.utils import rc

from stark.api import rest as rest_api
from stark.apps.commands import execute_command
from stark.apps.anima.models import Player, Message
from stark.apps.world.utils import draw_map
from stark.apps.timers import check_pulse

"""
Unlike the REST api, the command api is closely
tied to the UI client.

LoadHandler is the initial loader that fetches all
information from the server and essentially 'starts
fresh' every time.

PulseHandler and UserInputHandler work together to
update the clent on what needs to be changed. They
aim to only return data that has changed since the
last request.
The client is responsible for merging the new data
with the existing one.

The object responsible on the client side to hold
all of the data is a dictionary composed of 4 keys:
- map
- room
- player
- log

The API determines what part of the tree needs to
be changed and returns it to the client side. The
four utility functions are each responsible for
fetching their bit of the tree.
"""

# global caching switch.
PREVENT_CACHING = False

# utility function that creates a stark object with the specified nodes
class Fetcher(object):
    def __init__(self, request, player, cache=False, *args, **kwargs):
        super(Fetcher, self).__init__(*args, **kwargs)
        self.request = request
        self.player = player
        if PREVENT_CACHING:
            self.cache = False
        else:
            self.cache = cache

    def fetch(self, node_list):
        # NB: the order matters.... map needs to be after player so that the
        # coordinates it pulls are up to date
        stark = {}
        for node in node_list:
            fetched_node = getattr(self, "get_%s" % node)()
            if fetched_node is not None:
                stark[node] = fetched_node
        if not stark: # everything is cached correctly scenario
            return 'OK'
        return stark

    def get_map(self):
        """
        This will return a map centered around the player either when
        nothing is being cached (for example on initial load) or when
        the player gets too far away from the center.
        """
        if not self.cache:
            self.player.map_center_x = self.player.room.xpos
            self.player.map_center_y = self.player.room.ypos
            self.player.save()
            return draw_map(self.player.room.xpos,
                            self.player.room.ypos,
                            self.player.map_width)
        
        moved = False
        if abs(self.player.room.xpos - self.player.map_center_x) >= 3:
            self.player.map_center_x = self.player.room.xpos
            moved = True
        if abs(self.player.room.ypos - self.player.map_center_y) >= 3:
            self.player.map_center_y = self.player.room.ypos
            moved = True
        if moved:
            self.player.save()            
            return draw_map(self.player.map_center_x,
                            self.player.map_center_y,
                            self.player.map_width)
        return None
    
    def get_room(self):
        room = rest_api.RoomHandler().read(self.request,
                                           id=self.player.room.id)
        output = {
            'room': room,
            'signature': '0-0-0-0',
        }
        
        if not self.cache:
            return output
        
        # room caching is based on id and
        # comparing player, mobs and items presence in the room
        current_sig = getattr(self.request, self.request.method).get('room_sig')
        if current_sig:
            new_sig = "%s-%s-%s-%s" % (
                room.id,
                sum(room.player_related.all().values_list('id', flat=True)),
                sum(room.mob_related.all().values_list('id', flat=True)),
                sum(room.items.all().values_list('id', flat=True)),
            )
            if current_sig == new_sig:
                return None
            
            output['signature'] = new_sig
        
        return output

    def get_player(self):
        player = rest_api.PlayerHandler().read(self.request, self.player.id)

        output = {
            'player': player,
            'signature': '0',
        }
        
        if not self.cache:
            return output

        # player caching is based on level, hp, mp, inventory & equipment
        current_sig = getattr(self.request, self.request.method).get('player_sig')
        if current_sig:
            new_sig = "%s-%s-%s-%s-%s" % (
                player.level,
                player.hp,
                player.mp,
                sum(map(lambda x: x.id, player.inventory)),
                sum([i.id for i in player.equipment.values() if i]),
            )
            if current_sig == new_sig:
                return None
            
            output['signature'] = new_sig
        
        return output
        
    def get_log(self):
        messages = rest_api.MessageHandler().read(self.request)

        if not self.cache:
            return messages

        # caching scenarios
        last_log = getattr(self.request, self.request.method).get('last_log')
        if last_log == "0" and not messages:
            # the client says they have nothing and we have nothing
            return None
        if last_log:
            try:
                message = messages.get(pk=last_log)
                timestamp = message.created
                new_messages = messages.filter(created__gt=timestamp)
                if not new_messages:
                    return None
                else:
                    return messages
                    # return the messages that weren't yet included
                    return new_messages
            except Message.DoesNotExist:
                # that message ID doesn't even exist, refresh with what there is
                return messages

        if not messages:
            return None

        return messages

class UserInputHandler(BaseHandler):
    allowed_methods = ('POST',)
    
    def create(self, request):
        try:
            # get the player
            player = Player.objects.get(user=request.user, status='logged_in')
    
            # get the raw command
            raw_cmd = request.POST.get('command')

            # execute the command
            deltas = execute_command(player, raw_cmd)
            deltas.append('map')
            return Fetcher(request, player, cache=True).fetch(deltas)

        except Exception, e:
            error = "Command Error: %s" % e
            pulse_log = logging.getLogger('StarkLogger')
            pulse_log.debug(error)
            print error
            raise
    
class LoadHandler(BaseHandler):
    allowed_method = ('GET',)
    
    def read(self, request):
        player = Player.objects.get(user=request.user, status='logged_in')
        return Fetcher(request, player).fetch(['room',
                                               'player',
                                               'log',
                                               'map'])
        
class PulseHandler(BaseHandler):
    allowed_method = ('GET',)
    
    def read(self, request):
        check_pulse()
        player = Player.objects.get(user=request.user, status='logged_in')
        return Fetcher(request, player, cache=True).fetch(['log',
                                                           'room',
                                                           'player',
                                                           'map'])
