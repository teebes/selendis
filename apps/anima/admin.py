from django.contrib import admin
from stark.apps.anima.models import Player, Mob, MobLoader

class PlayerAdmin(admin.ModelAdmin): pass
class MobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template', 'room')
class MobLoaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template_mob')
    exclude = ('spawned_mobs',)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Mob, MobAdmin)
admin.site.register(MobLoader, MobLoaderAdmin)