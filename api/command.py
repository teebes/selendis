import datetime
import logging

from piston.handler import BaseHandler
from piston.utils import rc

from stark.api import handlers as rest_api
from stark.apps import commands
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
        stark = {}
        for node in node_list:
            fetched_node = getattr(self, "get_%s" % node)()
            if fetched_node is not None:
                stark[node] = fetched_node
        if not stark: # everything is cached correctly scenario
            return rc.ALL_OK
        return stark

    def get_map(self):
        return draw_map(0, 0, 10)
    
    def get_room(self):
        room = rest_api.RoomHandler().read(self.request,
                                           id=self.player.room.id)
        output = {
            'room': room,
            'signature': '0-0-0',
        }
        
        if not self.cache:
            return output
        
        # room caching is based on comparing player, mobs and items presence
        current_sig = getattr(self.request, self.request.method).get('room_sig')
        if current_sig:
            new_sig = "%s-%s-%s" % (
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
    
            # split the command into tokens, ignoring extra blank spaces
            tokens = filter(None, raw_cmd.split(' '))
    
            # grab the command name
            sub = tokens.pop(0)
            
            # TODO: move these aliases to defaults in a broader alias system
            if sub == 'n': sub = 'north'
            if sub == 'e': sub = 'east'
            if sub == 's': sub = 'south'
            if sub == 'w': sub = 'west'

            # convert sub to correctly formatted class name
            class_name = sub[0].upper() + sub[1:].lower()
    
            # get the command object
            if sub in commands.register or \
               (player.builder_mode and sub in commands.builder_register):
                cmd_class = getattr(commands, class_name)
            else:
                return "%s\nInvalid command: '%s'" % (raw_cmd, sub)
        
            # instanciate the command class
            cmd_instance = cmd_class(player, raw_cmd, tokens=tokens)

            # execute the command object
            deltas = cmd_instance.execute()
            
            # return the delta object
            return Fetcher(request, player).fetch(deltas)
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
        return Fetcher(request, player).fetch(['map', 'room', 'player', 'log'])
        
class PulseHandler(BaseHandler):
    allowed_method = ('GET',)
    
    def read(self, request):
        check_pulse()
        player = Player.objects.get(user=request.user, status='logged_in')
        return Fetcher(request, player, cache=True).fetch(['log', 'room', 'player'])
