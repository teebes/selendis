from django.conf.urls.defaults import *
from piston.resource import Resource
from stark.api.handlers import CommandHandler, ItemHandler, MapHandler, MeHandler, MessageHandler, PingHandler, PlayerHandler, RoomHandler


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

    
    #url(r'^players/me\.(?P<emitter_format>.+)', Resource(PlayerHandler)),
    url(r'^players/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', Resource(PlayerHandler)),
    
    url(r'^me\.(?P<emitter_format>.+)?$', Resource(MeHandler)),

    url(r'^messages\.(?P<emitter_format>.+)', Resource(MessageHandler)),
    
    url(r'^ping/$', Resource(PingHandler)),

    # UI APIs
    # - pulse
    # - command
    # - load
    
    url(r'^command/$', Resource(CommandHandler)),#, { 'emitter_format': 'json' }),
    
)
