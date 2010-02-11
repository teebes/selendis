import datetime
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from stark.apps.anima.constants import WEAPON_SLOTS, ARMOR_SLOTS
from stark.apps.world.constants import CONNECTOR_TYPES, DIRECTIONS, ROOM_TYPES, WEAPON_CLASSES

class Zone(models.Model):
    name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return "%s" % (self.name,)

class RoomConnector(models.Model):
    from_room = models.ForeignKey('Room', related_name='from_room')
    to_room = models.ForeignKey('Room', related_name='to_room')
    type = models.CharField(max_length=40, choices=CONNECTOR_TYPES)
    direction = models.CharField(max_length=40, choices=DIRECTIONS)

class Room(models.Model):
    zone = models.ForeignKey(Zone, related_name='rooms')
    xpos = models.IntegerField()
    ypos = models.IntegerField()
    name = models.CharField(max_length=80, blank=False)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    
    connected_rooms = models.ManyToManyField(
                                'self',
                                through='RoomConnector',
                                symmetrical=False)

    items = generic.GenericRelation('ItemInstance',
                                    object_id_field='owner_id',
                                    content_type_field='owner_type')

    def notify(self, msg, source=None, target=None, exclude=None):
        """
        Notifies all player in the room, except for the source and/or
        target, if specified.
        If provided, source/target must be a dictionary of the format:
            {
                'anima': <anima that needs a special message>,
                'message': <message to be displayed instead>,
            }
        If provided, exclude will skip the provided player or list of players
        """

        # normalize exlcude input
        if exclude and (type(exclude) not in (list, dict)):
            exclude = [exclude]

        for player in self.player_related.all():
            if exclude and player in exclude:
                continue
            
            if source and player == source['anima']:
                player.notify(source['message'])
            elif target and player == target['anima']:
                player.notify(target['message'])
            else:
                player.notify(msg)

    def get_name(self):
        return u"%s" % self.name

    def __unicode__(self):
        return u"%s, %s: %s" % (self.xpos, self.ypos, self.name )

"""
class RoomTracker(models.Model):
    room = ForeignKey(Room, related_name='tracker')
    
    content_type = models.ForeignKey(ContentType)
    content_id = models.PositiveIntegerField()
    content = generic.GenericForeignKey('content_type', 'content_id')
    
    created = models.DateTimeField(editable=False)
    #modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.now()
        #self.modified = datetime.datetime.now()
        superRoom(Tracker, self).save(*args, **kwargs)
"""

class BaseItem(models.Model):
    # 
    # - effect type
    # - effect value    
    
    class Meta:
        abstract = True
    
    capacity = models.IntegerField(default=0)
    name = models.CharField(max_length=40, blank=False)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.01"))
    modifiers = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        return "%s" % (self.name)

_WEAPON_SLOTS = map(lambda x: (x, x), WEAPON_SLOTS)
class Weapon(BaseItem):
    # damage is expressed with dice rolls, in the standard form AdX,
    # A being the number of dice to be rolled
    # X being the number of faces of the dice
    num_dice = models.IntegerField(blank=False)
    num_faces = models.IntegerField(blank=False)
    weapon_class = models.CharField(max_length=20, choices=WEAPON_CLASSES)
    two_handed = models.BooleanField(default=False)
    slot = models.CharField(max_length=40, choices=_WEAPON_SLOTS, blank=False)
    hit_first = models.CharField(max_length=20, blank=True)
    hit_third = models.CharField(max_length=20, blank=True)
    
    def hit_messages(self):
        if self.hit_first:
            if self.hit_third:
                return [self.hit_first, self.hit_third]
            else:
                return [self.hit_first, "%ss" % self.hit_first]
                
        # try the weapon defaults
        if self.weapon_class == 'short_blade':
            return ['stab', 'stabs']
        if self.weapon_class in ('medium_blade', 'long_blade'):
            return ['slash', 'slashes']
        elif self.weapon_class == 'spear':
            return ['strike', 'strikes']
        elif self.weapon_class == 'chain':
            return ['whip', 'whips']
        elif self.weapon_class == 'projectile':
            return ['throw', 'throws']
        elif self.weapon_class == 'axe':
            return ['hack', 'hacks']

        return ['hit', 'hits']

class Equipment(BaseItem):
    """This class is deperacted, 'Equipment' is now Armor + Weapons"""
    slot = models.CharField(max_length=40, choices=[], blank=False)

_ARMOR_SLOTS = map(lambda x: (x, x), ARMOR_SLOTS)
class Armor(BaseItem):    
    slot = models.CharField(max_length=40, choices=_ARMOR_SLOTS, blank=False)
    absorption = models.IntegerField(default=0)

class Sustenance(BaseItem): pass

class Misc(BaseItem): pass

class ItemManager(models.Manager):
    def owned_by(self, owner):
        return super(ItemManager, self).filter(
                owner_type__name = owner.__class__.__name__.lower(),
                owner_id = owner.id,
        )

class ItemInstance(models.Model):
    # these are the true physical objects that players can hold in their
    # inventory, equip, eat, etc. Each instance is of an item of the four basic
    # types
    
    name = models.CharField(max_length=40, blank=True)
    
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
    
    objects = ItemManager()
    
    modified = models.DateTimeField(blank=True)
    
    @property
    def capacity(self):
        return self.base.capacity
    
    def delete(self, *args, **kwargs):
        # if deleted, recursively delete all contained items
        if self.base.capacity > 0:
            ItemInstance.objects.owned_by(self).delete()
        super(ItemInstance, self).delete(*args, **kwargs)
    
    def get_name(self):
        name = self.name
        if not name:
            name = self.base.name
        return name
    
    def total_weight(self, weight=0):
        # weight including contained items (recursive)
        weight += self.base.weight
        if self.base.capacity > 0:
            for contained_item in ItemInstance.objects.owned_by(self):
                weight += contained_item.total_weight()
        return weight    
    
    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        super(ItemInstance, self).save(*args, **kwargs)
    
    def __unicode__(self):
        name = self.get_name()
        
        # items carried by players / mobs
        if self.owner_type.name in ('player', 'mob'):
            return u"%s, carried by %s" % (name, self.owner.get_name())

        # item lying in room
        elif self.owner_type.name == 'room':
            return u"%s, on the ground in %s" % (name, self.owner.get_name())

        # items in containers
        elif self.owner_type.name == 'item instance':
            return u"%s, contained by %s" % (name, self.owner.get_name())

        return u"%s" % (name)
