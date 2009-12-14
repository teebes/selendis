from django.contrib import admin
from stark.apps.world.models import Equipment, ItemInstance, Misc, Room, Sustenance, Weapon

from django.contrib.contenttypes import generic


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'xpos',
        'ypos',
        'name',
    )

class EquipmentAdmin(admin.ModelAdmin): pass
class MiscAdmin(admin.ModelAdmin): pass
class SustenanceAdmin(admin.ModelAdmin): pass
class WeaponAdmin(admin.ModelAdmin): pass

class ItemInstanceInline(generic.GenericTabularInline):
    model = ItemInstance
    ct_field = 'owner_type'
    ct_fk_field = 'owner_id'

class ItemInstanceAdmin(admin.ModelAdmin):
    inlines = [
        ItemInstanceInline,
    ]

# registers
admin.site.register(Room, RoomAdmin)

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Misc, MiscAdmin)
admin.site.register(Sustenance, SustenanceAdmin)
admin.site.register(Weapon, WeaponAdmin)

admin.site.register(ItemInstance, ItemInstanceAdmin)
