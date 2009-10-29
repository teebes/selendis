from django.contrib import admin
from stark.apps.anima.models import Player, Mob

class PlayerAdmin(admin.ModelAdmin): pass
class MobAdmin(admin.ModelAdmin): pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Mob, MobAdmin)
