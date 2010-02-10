import datetime
import logging
import random

from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models, transaction

from stark import config
from stark.apps.anima import constants as anima_constants
from stark.apps.anima.combat import determine_attack_outcome
from stark.apps.anima.constants import PLAYER_STATUSES, MESSAGE_TYPES, MOB_TYPES, ARMOR_SLOTS, WEAPON_SLOTS
from stark.apps.world.models import Room, RoomConnector, ItemInstance, Weapon, Armor, Misc, Sustenance
from stark.apps.world.utils import find_items_in_container
from stark.utils import roll_percent

MOVE_COST = 2 #TODO: move to global config

class Anima(models.Model):
    # name should be unique for player subclass (not enforced @ db level)
    name = models.CharField(max_length=40)
    room = models.ForeignKey(Room, related_name="%(class)s_related")

    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=1)
    next_level = models.IntegerField(default=1)
    
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    messages =  generic.GenericRelation('Message')
    
    hp = models.IntegerField(default=1)
    hp_base = models.IntegerField(default=1)
    mp = models.IntegerField(default=40)
    mp_base = models.IntegerField(default=40)
    sp = models.IntegerField(default=1)
    sp_base = models.IntegerField(default=1)
    
    strength = models.IntegerField(default=10)
    agility = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    
    # equipment (weapons + armor)
    main_hand = models.ForeignKey(ItemInstance,
                                  related_name="%(class)s_mainhand",
                                  blank=True, null=True)
        
    head = models.ForeignKey(ItemInstance,
                                related_name="%(class)s_head",
                                blank=True, null=True)
    
    chest = models.ForeignKey(ItemInstance,
                                 related_name="%(class)s_chest",
                                 blank=True, null=True)
    
    arms = models.ForeignKey(ItemInstance,
                                related_name="%(class)s_arms",
                                blank=True, null=True)

    hands = models.ForeignKey(ItemInstance,
                                related_name="%(class)s_hands",
                                blank=True, null=True)
    
    legs = models.ForeignKey(ItemInstance,
                                related_name="%(class)s_legs",
                                blank=True, null=True)

    feet = models.ForeignKey(ItemInstance,
                                related_name="%(class)s_feet",
                                blank=True, null=True)

    target_type = models.ForeignKey(ContentType, blank=True, null=True)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = generic.GenericForeignKey('target_type', 'target_id')

    @property
    def max_hp(self):
        # remember when changing this formula to also change it
        # in anima.utils.tick_regen()
        return self.hp_base + self.constitution * 5 + (self.level - 1) * 10
    
    @property
    def max_mp(self):
        return self.mp_base
    
    @property
    def capacity(self): return 10 * self.strength

    @property
    def equipment(self):
        eq = {}
        for attr in ARMOR_SLOTS + WEAPON_SLOTS:
            item = getattr(self, attr)
            if item:
                eq[attr] = item
            else:
                # ensures that the api calls don't return the string 'None'
                eq[attr] = ''
        return eq

    @property
    def inventory(self):
        equipment = self.equipment
        inv = []
        for item in ItemInstance.objects.owned_by(self):
            if item not in equipment.values():
                inv.append(item)
        return inv

    #############
    # Utilities #
    #############
    def notify(self, msg):
        Message.objects.create(type='notification',
                               destination=self.name,
                               content=msg)

    def regen(self, attribute, points):
        """
        Regen player attribtue (hp, mp or sp) by x point.
        """
        # no regen while in combat
        if self.target:
          return

        max = getattr(self, 'max_' + attribute)
        new = getattr(self, attribute) + points
        if new > max:
            new = max
        setattr(self, attribute, new)
        self.save()



    def get_name(self):
        # method to match ItemInstance's
        return self.name

    def update_level(self):
        levels = Level.objects.all()
        
        # update level if necessary
        level = levels.filter(requirement__lt=self.experience)\
                      .order_by('-id')[0]
        print "%s#%s" % (level, self.level)
        if level.id > self.level:
            self.notify('You gain a level!')
            self.level = level.id
            
        next_levels = levels.filter(requirement__gt=self.experience)\
                            .order_by('id')
        if len(next_levels) == 0: # last level, set 0 tnl
            self.next_level = self.experience
        else: # get tnl from the next level
            self.next_level = next_levels[0].requirement

        self.save()

    ##########
    # Combat #
    ##########
    
    def combat_round(self):
        """Runs an actual combat round as called by the events app"""
        # make sure source and target are in the same room
        if self.target.room != self.room:
            self.target = None
            return
        
        # if the target is not engaged on something else, source becomes
        # target's target
        if not self.target.target:
            self.target.target = self
            self.target.save()
        
        self.attack(self.target)
    
    def attack(self, target):
        
        # protect template mobs (I've had some bad experiences... this is
        # necessary)
        if getattr(target, 'template', False):
            self.notify("You can't harm template mobs.")
            self.target.target = None
            self.target.save()
            self.target = None
            self.save()
            return
        
        # pluggable function to determine the outcome of a round
        (hit, damage) = determine_attack_outcome(self, target)
        
        # get the hit messages from the weapon, if applicable
        hit_messages = ['hit', 'hits']
        if self.main_hand:
            hit_messages = self.main_hand.base.hit_messages()
        
        # send notifications
        for player in self.room.player_related.all():
            if player == self: # attacker
                if hit:
                    msg = "[%s dmg dealt] You %s %s." % \
                            (damage, hit_messages[0], target.name)
                else:
                    msg = "%s defends against your attack." % target.name
                player.notify(msg)
            elif player == target: # defender
                if hit:
                    msg = "[%s dmg taken] %s %s you." % \
                              (damage, self.name, hit_messages[1])
                else:
                    msg = "You defend against %s's attack" % self.name                    
                player.notify(msg)
            else: # bystander
                if hit:
                    msg = ("%s %s %s" %
                              (self.name, hit_messages[1], target.name))
                else:
                    msg = "%s defends against %s' attack" \
                          (target.name, self.name)
                player.notify(msg)

        # record the hit, if applicable
        if hit:
            target.hp -= damage
            target.save()
    
            # kill the target if applicable
            if target.hp <= 0:
                target.die(killer=self)
                self.target = None
                self.save()
                self.update_level()

    def die(self):
        # Anima and Mob each call this as supers of the overwritten method
        for room_player in self.room.player_related.all():
            if room_player != self:
                room_player.notify("%s is dead!" % self.name)

        # create a corpse
        corpse = ItemInstance.objects.create(base=Misc.objects.get(pk=1),
                                             owner=self.room,
                                             name='the corpse of %s' %
                                                    self.name)
        
        # transfer all items to the corpse
        for item in ItemInstance.objects.owned_by(self):
            item.owner = corpse
            item.save()

    ################
    # Django stuff #
    ################

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        ItemInstance.objects.owned_by(self).delete()
        super(Anima, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name

class Player(Anima):
    user = models.ForeignKey(User, related_name='players')
    builder_mode = models.BooleanField(default=False)
    temporary = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PLAYER_STATUSES)
    last_activity = models.DateTimeField(blank=True, null=True)

    def die(self, killer=None):
        self.target = None
        self.hp = 1
        
        death_room_id = getattr(config, 'DEATH_ROOM_ID', 1)
        try:
            death_room = Room.objects.get(pk=death_room_id)
        except Room.DoesNotExist:
            raise Exception("There must be a room with pk=1")
        self.room = death_room
        self.save()
        
        self.notify("You are dead! Sorry...")

        super(Player, self).die()
    
    def save(self, *args, **kwargs):
        self.last_activity = datetime.datetime.now()
        return super(Player, self).save(*args, **kwargs)

class Mob(Anima):
    # static mobs can't move
    static = models.BooleanField(default=False)

    # these are template mobs from which other mobs get created
    template = models.BooleanField(default=False)
    
    def notify(self, *args, **kwargs): pass

    def die(self, killer=None):
        
        if self.template:
            raise Exception("You can't kill template mobs!")
        
        if killer:
            killer.experience += self.experience
            killer.save()
        
        super(Mob, self).die()
        
        self.delete()


class MobLoader(models.Model):
    # optional name for the loader
    name = models.CharField(max_length=20, blank=True, null=True)

    # spawn control
    batch_size = models.IntegerField(default=1)
    spawn_chance = models.IntegerField(default=100)
    zone_limit = models.IntegerField(default=1)
    
    # mob tracking
    template_mob = models.ForeignKey(Mob, related_name='loaders')
    spawned_mobs = models.ManyToManyField(Mob, blank=True)

    # items
    armor = models.ManyToManyField(Armor, blank=True)
    weapon = models.ManyToManyField(Weapon, blank=True)
    misc = models.ManyToManyField(Misc, blank=True)
    sustenance = models.ManyToManyField(Sustenance, blank=True)
    
    notes = models.TextField(blank=True)
    
    # rooms
    spawn_in = models.ManyToManyField(Room)
    
    def run(self):
        # check to see if a load needs to happen
        if self.spawned_mobs.count() >= self.zone_limit:
            return
        
        for i in range(0, self.batch_size):
            if not roll_percent(self.spawn_chance):
                break
            for room in self.spawn_in.all():

                mob = self.template_mob
                mob.id = None
                mob.template = False
                mob.room = Room.objects.get(pk=1)
                mob.save()

                for attribute in ['armor', 'weapon', 'misc', 'sustenance']:
                    for base in getattr(self, attribute).all():
                        item = ItemInstance.objects.create(owner = mob,
                                                           base = base)
                        # if there is a free space in a slot, wear the item
                        if not getattr(mob, item.base.slot):
                            setattr(mob, item.base.slot, item)

                mob.hp = mob.max_hp
    
                mob.room = room
                mob.save()

                self.spawned_mobs.add(mob)

    
class Message(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now,
                                   blank=False)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPES, blank=False)
    content = models.TextField(blank=False)
    destination = models.CharField(max_length=40, blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    author = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return u"%s: %s" % (self.author, self.content)

class Level(models.Model):
    requirement = models.IntegerField()
    """
    def get_level_for_exp(experience):
        # returns a tuple (level, next exp requirement)
    
        for level in sorted(LEVELS, reverse=True):
            (number, requirement) = level
            if experience > requirement:
                if level == LEVELS[-1]: # last level, return 0 tnl
                    return (number, requirement)
                else:
                    return (number, LEVELS[LEVELS.index(level) + 2][1])
        
        # if a user didn't get a level for any exp, then the levels are
        # misconfigured
        raise Exception('Levels are misconfigured')    
    """
    def __unicode__(self):
        return u"level %s, %s exp" % (self.id, self.requirement)
       
 
