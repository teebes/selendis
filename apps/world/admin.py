from django.contrib import admin
from stark.apps.world.models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'xpos',
        'ypos',
        'title',
    )

admin.site.register(Room, RoomAdmin)
