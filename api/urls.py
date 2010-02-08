from django.conf.urls.defaults import *
from piston.resource import Resource
from stark.api.handlers import ItemHandler, MapHandler, MessageHandler, PingHandler, PlayerHandler, RoomHandler
from stark.api import command as command_api

urlpatterns = patterns('',
    # world APIs
    
    # deprecated (removing the 'world' of the URL over time)
    url(r'^world/items/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(ItemHandler)),
    url(r'^world/rooms/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(RoomHandler)),
    url(r'^world/rooms/create/', Resource(RoomHandler)),
    url(r'^world/map\.(?P<emitter_format>.+)', Resource(MapHandler)),

    url(r'^items/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(ItemHandler)),
    url(r'^rooms/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(RoomHandler)),
    url(r'^rooms/create/', Resource(RoomHandler)),
    url(r'^map\.(?P<emitter_format>.+)', Resource(MapHandler)),

    
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
