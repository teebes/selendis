from django.contrib import admin
from stark.apps.anima.models import Player, Mob, MobLoader

class PlayerAdmin(admin.ModelAdmin): pass
class MobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template', 'room')
    list_editable = ('room',)
class MobLoaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template_mob')
    exclude = ('spawned_mobs',)
    filter_horizontal = ('armor', 'weapon', 'misc', 'sustenance', 'spawn_in')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "template_mob":
            kwargs["queryset"] = Mob.objects.filter(template=True)
            return db_field.formfield(**kwargs)
        return super(MobLoaderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    
admin.site.register(Player, PlayerAdmin)
admin.site.register(Mob, MobAdmin)
admin.site.register(MobLoader, MobLoaderAdmin)