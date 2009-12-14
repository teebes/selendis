from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from stark.apps.world.constants import CONNECTOR_TYPES, DIRECTIONS, ROOM_TYPES, WEAPON_CLASSES
    
class RoomConnector(models.Model):
    from_room = models.ForeignKey('Room', related_name='from_room')
    to_room = models.ForeignKey('Room', related_name='to_room')
    type = models.CharField(max_length=40, choices=CONNECTOR_TYPES)
    direction = models.CharField(max_length=40, choices=DIRECTIONS)

class Room(models.Model):
    xpos = models.IntegerField(blank=False)
    ypos = models.IntegerField(blank=False)
    #title = models.CharField(max_length=80, blank=False)
    name = models.CharField(max_length=80, blank=False)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    
    connected_rooms = models.ManyToManyField(
                                'self',
                                through='RoomConnector',
                                symmetrical=False)

    items = generic.GenericRelation('ItemInstance',
                                    object_id_field='owner_id',
                                    content_type_field='owner_type')

    def notify(self, msg):
        for player in self.player_related.all():
            player.notify(msg)

    def __unicode__(self):
        return u"%s, %s: %s" % (self.xpos, self.ypos, self.title)


class BaseItem(models.Model):
    # 
    # - effect type
    # - effect value    
    
    class Meta:
        abstract = True
    
    capacity = models.IntegerField(default=0)
    name = models.CharField(max_length=40, blank=False)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.01"))
    
    def __unicode__(self):
        return "%s" % (self.name)
    
class Weapon(BaseItem):
    # damage is expressed with dice rolls, in the standard form AdX,
    # A being the number of dice to be rolled
    # X being the number of faces of the dice
    num_dice = models.IntegerField(blank=False)
    num_faces = models.IntegerField(blank=False)
    weapon_class = models.CharField(max_length=20, choices=WEAPON_CLASSES)
    two_handed = models.BooleanField(default=False)
    

class Equipment(BaseItem): pass

class Sustenance(BaseItem): pass

class Misc(BaseItem): pass

class ItemInstance(models.Model):
    # these are the true physical objects that players can hold in their
    # inventory, equip, eat, etc. Each instance is of an item of the four basic
    # types
    
    # the player, mob or room currently holding the item
    owner_type = models.ForeignKey(ContentType, related_name='owner')
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    owns = generic.GenericRelation('ItemInstance',
                                   object_id_field='owner_id',
                                   content_type_field='owner_type')

    # which item this instance is derived from
    base_type = models.ForeignKey(ContentType, related_name='base')
    base_id = models.PositiveIntegerField()
    base = generic.GenericForeignKey('base_type', 'base_id')
    
    def __unicode__(self):
        # items carried by players / mobs
        if self.owner_type.name in ('player', 'mob'):
            return u"%s, carried by %s" % (self.base.name, self.owner.name)

        # item lying in room
        elif self.owner_type.name == 'room':
            return u"%s, on the ground in %s" % (self.base.name, self.owner.name)

        # items in containers
        elif self.owner_type.name == 'item instance':
            return u"%s, contained by %s #%s" % (self.base.name, self.owner_type.name, self.owner.id)

        return u"%s" % (self.base.name)
