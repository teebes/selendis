from django.conf.urls.defaults import *
from piston.resource import Resource
from stark.api.handlers import MapHandler, PlayerHandler, RoomHandler, PingHandler, MessageHandler, ItemHandler

urlpatterns = patterns('',
    url(r'^world/items/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(ItemHandler)),

    url(r'^world/rooms/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(RoomHandler)),
    url(r'^world/rooms/create/', Resource(RoomHandler)),
    url(r'^world/map\.(?P<emitter_format>.+)', Resource(MapHandler)),

    
    url(r'^players/me\.(?P<emitter_format>.+)', Resource(PlayerHandler)),
    url(r'^players/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(PlayerHandler)),

    url(r'^messages\.(?P<emitter_format>.+)', Resource(MessageHandler)),
    
    url(r'^ping.(?P<emitter_format>.+)$', Resource(PingHandler)),

    
)
