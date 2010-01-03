from django.contrib import admin
from stark.apps.world.models import Armor, ItemInstance, Misc, Room, Sustenance, Weapon, Zone

from django.contrib.contenttypes import generic

class ZoneAdmin(admin.ModelAdmin): pass

class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'xpos',
        'ypos',
        'name',
    )

#class EquipmentAdmin(admin.ModelAdmin): pass

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'capacity', 'weight']

class MiscAdmin(ItemAdmin): pass
class SustenanceAdmin(ItemAdmin): pass
class WeaponAdmin(ItemAdmin):
    def __init__(self, *args, **kwargs):
        super(WeaponAdmin, self).__init__(*args, **kwargs)
        self.list_display += ['slot']
class ArmorAdmin(ItemAdmin):
    def __init__(self, *args, **kwargs):
        super(ArmorAdmin, self).__init__(*args, **kwargs)
        self.list_display += ['slot']
class ItemInstanceInline(generic.GenericTabularInline):
    model = ItemInstance
    ct_field = 'owner_type'
    ct_fk_field = 'owner_id'

class ItemInstanceAdmin(admin.ModelAdmin):
    inlines = [
        ItemInstanceInline,
    ]

# registers
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Room, RoomAdmin)

admin.site.register(Armor, ArmorAdmin)
admin.site.register(Misc, MiscAdmin)
admin.site.register(Sustenance, SustenanceAdmin)
admin.site.register(Weapon, WeaponAdmin)

admin.site.register(ItemInstance, ItemInstanceAdmin)
