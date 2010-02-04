from piston.handler import BaseHandler
from piston.utils import rc

from stark.api import handlers as rest_api
from stark.apps.anima.models import Player
from stark.apps.world.utils import draw_map

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

# utility function that creates a stark object with the specified nodes
class Fetcher(object):
    def __init__(self, request, player, *args, **kwargs):
        super(Fetcher, self).__init__(*args, **kwargs)
        self.request = request
        self.player = player

    def fetch(self, node_list):
        stark = {}
        for node in node_list:
            try:
                stark[node] = getattr(self, "get_%s" % node)()
            except AttributeError:
                pass
        return stark

    def get_map(self):
        return draw_map(0, 0, 10)
    
    def get_room(self):
        return rest_api.RoomHandler().read(self.request,
                                           id=self.player.room.id)

    def get_player(self):
        return rest_api.MeHandler().read(self.request)
        
    def get_log(self):
        return rest_api.MessageHandler().read(self.request)

class UserInputHandler(BaseHandler):
    allowed_methods = ('POST',)
    
    def create(self, request):
        player = Player.objects.get(user=request.user, status='logged_in')
        output = player.command(request.POST.get('command'))
        if output is None:
            # temporary stopgap for the commands that are not returning
            # anything
            output = ['log']
        return Fetcher(request, player).fetch(output)
    
class LoadHandler(BaseHandler):
    allowed_method = ('GET',)
    
    def read(self, request):
        player = Player.objects.get(user=request.user, status='logged_in')
        return Fetcher(request, player).fetch(['map', 'room', 'player', 'log'])
        
class PulseHandler(BaseHandler):
    allowed_method = ('GET',)
    
    def read(self, request):
        player = Player.objects.get(user=request.user, status='logged_in')
        return Fetcher(request, player).fetch(['log', 'room', 'player'])
