from django.conf.urls.defaults import *
from piston.resource import Resource
from stark.api.handlers import MapHandler, PlayerHandler, RoomHandler, PingHandler

player_handler = Resource(PlayerHandler)

urlpatterns = patterns('',
    url(r'^world/rooms/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(RoomHandler)),
    url(r'^world/map\.(?P<emitter_format>.+)', Resource(MapHandler)),
    
    url(r'^players/me\.(?P<emitter_format>.+)', player_handler),
    url(r'^players/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', player_handler),
    
    url(r'^ping.(?P<emitter_format>.+)$', Resource(PingHandler)),

    
)
