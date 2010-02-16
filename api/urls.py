from django.conf.urls.defaults import *
from piston.resource import Resource
from stark.api.rest import ItemHandler, MapHandler, MessageHandler, PingHandler, PlayerHandler, PreferencesHandler, RoomHandler
from stark.api import command as command_api

urlpatterns = patterns('',
    # rest API
    url(r'^items/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(ItemHandler)),
    url(r'^rooms/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(RoomHandler)),
    url(r'^rooms/create/', Resource(RoomHandler)),
    url(r'^map\.(?P<emitter_format>.+)', Resource(MapHandler)),
    url(r'^preferences(\.(?P<emitter_format>.+))?/$', Resource(PreferencesHandler)),

    url(r'^players/(?P<id>\d+)(\.(?P<emitter_format>.+))?/$', Resource(PlayerHandler)),

    url(r'^messages\.(?P<emitter_format>.+)', Resource(MessageHandler)),
    
    url(r'^ping/$', Resource(PingHandler)),

    # UI APIs
    # - pulse
    # - command
    # - load
    
    url(r'^command/$', Resource(command_api.UserInputHandler)),
    url(r'^load/$', Resource(command_api.LoadHandler)),
    url(r'^pulse/$', Resource(command_api.PulseHandler)),
)
