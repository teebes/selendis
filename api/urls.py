from django.conf.urls.defaults import *
from piston.resource import Resource
from stark.api.handlers import MapHandler, PlayerHandler, CommandHandler

player_handler = Resource(PlayerHandler)

urlpatterns = patterns('',
    url(r'^world/map\.(?P<emitter_format>.+)', Resource(MapHandler)),
    #url(r'^rooms/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', room_handler),
    
    url(r'^players/me\.(?P<emitter_format>.+)', player_handler),
    url(r'^players/((?P<id>[^/]+)\.(?P<emitter_format>.+))?$', player_handler),
    
    url(r'^commands/send\.(?P<emitter_format>.+)', Resource(CommandHandler)),
    
)
