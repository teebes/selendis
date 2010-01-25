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

    #############
    # Utilities #
    #############
    def notify(self, msg):
        Message.objects.create(type='notification',
                               destination=self.name,
                               content=msg)
    
    def move(self, xpos=None, ypos=None, to_room=None, random=False):
        
        if self.target:
            self.notify('You cannot move while in combat.')
            return
        
        # get the connector based on the input provided
        if xpos and ypos:
            try:
                connector = RoomConnector.objects.get(from_room=self.room,
                                                      to_room__xpos=xpos,
                                                      to_room__ypos=ypos)
            except RoomConnector.DoesNotExist:
                self.notify("You cannot go that way.")
                raise Exception("No connector exists to provied x/y coords")
        elif to_room:
            try:
                connector = RoomConnector.objects.get(from_room=self.room,
                                                      to_room=to_room)
            except RoomConnector.DoesNotExist:
                self.notify("You cannot go that way.")
                raise Exception("No connector exists to provided to_room")
        elif random:
            try:
                if self.__class__.__name__ == "Mob":
                    # by default keep mobs within zones
                    connector = RoomConnector.objects\
                                .filter(to_room__zone__id=self.room.zone.id,
                                        from_room=self.room)\
                                .order_by('?')[0]
                else:
                    connector = RoomConnector.objects\
                                .filter(from_room=self.room)\
                                .order_by('?')[0]
            except (RoomConnector.DoesNotExist, IndexError):
                # no exits, don't move at all
                return
                # raise Exception("No exit out of this room exists")
        else:
            raise Exception('provide either x/y coords or set random=True')

        to_room = connector.to_room

        # unless in builder mode, check for move points and deduct points
        if not (self.__class__.__name__ == 'Mob' or hasattr(self, 'builder_mode') and self.builder_mode == True):
            if self.mp < MOVE_COST:
                msg = "Not enough movement points to move."
                self.notify(msg)
                raise Exception(msg)
            else:
                self.mp -= MOVE_COST

        # store where the user was before the move
        from_room = self.room
        
        # move the user
        self.room = to_room

        # save
        self.save()
        
        # track this movement
        # RoomTracker.objects.create(room=self.room, content=self)
        
        # tell every player in the room the anima was in that it's gone
        for player in Player.objects.filter(room=from_room, status='logged_in'):
            player.notify("%s leaves %s." % (self.name, connector.direction))
        
        rev_direction = None
        if connector.direction == 'north': rev_direction = 'south'
        elif connector.direction == 'east': rev_direction = 'west'
        elif connector.direction == 'south': rev_direction = 'north'
        elif connector.direction == 'west': rev_direction = 'east'
            
        # tell every player in the room the anima is moving to that it's
        # arrived, or simply that it's moved if the observer is the one
        # performing the action
        for player in Player.objects.filter(room=to_room, status='logged_in'):
            if player == self:
                self.notify("You leave %s" % connector.direction)
            else:
                player.notify("%s has arrived from the %s." %
                                (self.name, rev_direction))                
    
    def regen(self, attribute, points):
        """
        Regen player attribtue (hp, mp or sp) by x points
        """
        max = getattr(self, 'max_' + attribute)
        new = getattr(self, attribute) + points
        if new > max:
            new = max
        setattr(self, attribute, new)
        self.save()


    def get_carrying_weight(self):
        weight = Decimal('0.00')
        for item in ItemInstance.objects.owned_by(self):
            weight += item.total_weight()
        return weight

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
    
    def engage(self, target_type, target_id):
        not_here = "No-one by that name."
        try:
            target_type = ContentType.objects.get(model=target_type)
            target = target_type.model_class().objects.get(pk=target_id)
            if self.room != target.room:
                self.notify(not_here)

            self.target = target
            self.save()
        except Exception:
            self.notify(not_here)
    
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

    #####################
    # Item Interactions #
    #####################

    def equipment(self):
        # returns dict
        eq = {}
        for attr in ARMOR_SLOTS + WEAPON_SLOTS:
            item = getattr(self, attr)
            if item:
                eq[attr] = item
            else:
                # ensures that the api calls don't return the string 'None'
                eq[attr] = ''
        return eq

    def inventory(self):
        # returns list
        equipment = self.equipment()
        inv = []
        for item in ItemInstance.objects.owned_by(self):
            if item not in equipment.values():
                inv.append(item)
        return inv

    def give_item(self, item, give_to):
        
        if item.owner.room != give_to.room:
            stark_log = logging.getLogger('StarkLogger')
            message = ("%s can't give item %s to %s because they aren't"
                       " in the same room" %
                        (self.name, item.name, give_to.name))
            stark_log.debug(message)
            raise Exception(message)

        print item.total_weight()
        print give_to.capacity
        # check that the user can carry the weight
        free_room = give_to.capacity - give_to.get_carrying_weight()
        if item.total_weight() > free_room:
            self.notify("%s cannot carry that much weight." % give_to.name)
            return

        item.owner = give_to
        item.save()

        for player in self.room.player_related.all():
            if player == self:
                self.notify("You give %s to %s." %
                            (item.base.name, give_to.name))
            elif player == give_to:
                give_to.notify("%s gives you %s." %
                               (self.name, item.base.name))
            else:
                player.notify("%s gives %s to %s" %
                              (self.name, item.base.name, give_to.name))

    def drop_item(self, item):
        item.owner = self.room
        item.save()
        for player in self.room.player_related.all():
            if player == self:
                self.notify("You drop %s." % item.base.name)
            else:
                player.notify("%s drops %s." % (self.name, item.base.name))

    def get_item(self, item):
        if item.owner != self.room:
            stark_log = logging.getLogger('StarkLogger')
            message = ("%s can't get item %s because they're in "
                       "different rooms" % (self.name, item.get_name()))
            stark_log.debug(message)
            raise Exception(message)

        # check that the user can carry the weight
        free_room = self.capacity - self.get_carrying_weight()
        if item.total_weight() > free_room:
            self.notify("%s is too heavy for you to pick up."
                        % item.get_name())
            return

        item.owner = self
        item.save()
        
        for player in self.room.player_related.all():
            if player == self:
                self.notify("You get %s." % item.base.name)
            else:
                player.notify("%s gets %s." % (self.name, item.base.name))

    def get_item_from_container(self, item):
        # container is in player or in player's room
        if (item.owner.owner.__class__ is Room and
            item.owner.owner == self.room) or \
           (item.owner.owner.__class__ is Player and
            item.owner.owner == self):

            # check that the user can carry the weight
            free_room = self.capacity - self.get_carrying_weight()
            if item.total_weight() > free_room:
                self.notify("%s is too heavy for you to pick up."
                            % item.get_name())
                return
            
            old_owner = item.owner

            item.owner = self
            item.save()

            for player in self.room.player_related.all():
                if player == self:
                    self.notify("You get %s from %s." % (
                        item.get_name(),
                        old_owner.get_name()
                    ))
                else:
                    player.notify("%s gets %s from %s." % (
                        self.name,
                        item.get_name(),
                        old_owner.get_name()
                    ))

        else:
            stark_log = logging.getLogger('StarkLogger')
            message = ("%s can't get item %s from container %s because "
                       "they're in different rooms" % (
                            self.name,
                            item.get_name(),
                            item.owner.get_name()
                       ))
            stark_log.debug(message)
            raise Exception(message)

    def put_item_in_container(self, item, container):
        # container is in the room or a player
        if (container.owner.__class__ is Room and container.owner == item.owner.room) or \
           (container.owner.__class__ is Player and container.owner == item.owner):
            
                for player in self.room.player_related.all():
                    if player == self:
                        self.notify("You put %s in %s." % \
                                    (item.base.name, container.base.name))
                    else:
                        player.notify("%s puts %s in %s." % \
                            (self.name, item.base.name, container.base.name))
            
                item.owner = container
                item.save()

        else:
            stark_log = logging.getLogger('StarkLogger')
            message = ("Can't put %s in %s because you don't have access"
                       "to it.") % (item.base.name, container.base.name)
            stark_log.debug(message)
            raise Exception(message)


    def wear(self, item, wear_verb='wear'):
        if item.base.__class__.__name__ == "Weapon":
            if wear_verb == 'wear':
                wear_verb = 'wield'
        
        if getattr(self, item.base.slot):
            self.notify("You're already wearing something on this slot.")
            return
        
        setattr(self, item.base.slot, item)
        self.save()
        
        for player in self.room.player_related.all():
            if player == self:
                self.notify("You %s %s." % (wear_verb, item.base.name))
            else:
                player.notify("%s %ss %s." % (self.name, wear_verb,
                                              item.base.name))

    def remove(self, item):        
        if not getattr(self, item.base.slot):
            self.notify("This slot is empty.")
            raise Exception("Slot empty")
            
        setattr(self, item.base.slot, None)
        self.save()
        
        for player in self.room.player_related.all():
            if player == self:
                self.notify("You remove %s." % item.base.name)
            else:
                player.notify("%s removes %s." % (self.name, item.base.name))

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

    ############
    # Commands #
    ############

    def command(self, cmd):
        tokens = map(lambda x: x.lower(), cmd.split(' '))

        # - help
        if tokens[0] == 'help':
            self.notify('Commands:')
            self.notify('- north east south west kill')
            self.notify('- get drop put wear wield remove')
            self.notify('- chat help')

        # - wear / wield -
        if tokens[0] in ('wear', 'wield'):
            if len(tokens) < 2:
                self.notify('Usage: wear item')
                return
            items = find_items_in_container(tokens[1], self.inventory())
            for item in items:
                self.wear(item)
            if not items:
                self.notify('You have no %s to wear.' % tokens[1])
                return

        # - remove -
        if tokens[0] == 'remove':
            if len(tokens) < 2:
                self.notify('Usage: remove item')
                return
            eq = filter(lambda x: x, self.equipment().values())
            items = find_items_in_container(tokens[1], eq)
            if items:
                self.remove(items[0])
            else:
                self.notify('You are not wearing a %s.' % tokens[1])
                return

        # - get -
        if tokens[0] == 'get':
            # simple get from room
            if len(tokens) == 0:
                self.notify('Usage: get item [container]')
                return
            elif len(tokens) == 2:
                items = find_items_in_container(tokens[1],
                                                self.room.items.all())
                for item in items:
                    self.get_item(item)
                if not items:
                    self.notify('There is no %s in this room.' % tokens[1])
                    return
            
            # get from container
            elif len(tokens) >= 3:
                # try to get the container from the player's equipment, inv
                # or the room
                eq = filter(lambda x: x, self.equipment().values())
                container = find_items_in_container(tokens[2], eq,
                                                    find_container=True)
                if not container:
                    container = find_items_in_container(tokens[2],
                                                        self.inventory(),
                                                        find_container=True)
                if not container:
                    container = find_items_in_container(tokens[2],
                                                        self.room.items.all(),
                                                        find_container=True)
                
                # if no suitable container has been found, raise eror
                if not container:
                    self.notify(error = 'No such container: %s' % tokens[2])
                    return
                
                # get the item from the found container
                # TODO: should this support getting stuff from
                # multiple container?
                items = find_items_in_container(tokens[1],
                                                container[0].owns.all())

                for item in items:
                    self.get_item_from_container(item)

                if not items:
                    self.notify('There is no %s in %s' %
                                    (tokens[1], tokens[2]))
                    return

        # - put -
        if tokens[0] == 'put':
            if len(tokens) < 3:
                self.notify("Usage: put item container")
                raise Exception('Not enough tokens for put command')
            else:
                # get the items that the user wants to put somewhere
                items = find_items_in_container(tokens[1], self.inventory())
                if not items:
                    self.notify('There is no %s in your inventory' % tokens[1])
                    return
                
                # get the best match from eq, inv and room
                eq = filter(lambda x: x, self.equipment().values())
                containers = find_items_in_container(tokens[2], eq,
                                                     find_container=True)
                if not containers:
                    containers = find_items_in_container(tokens[2],
                                                         self.inventory(),
                                                         find_container=True)
                if not containers:
                    containers = find_items_in_container(tokens[2],
                                                         self.room.items.all(),
                                                         find_container=True)
                if not containers:
                    self.notify('There is no %s in your inventory' % tokens[2])
                    return
                
                for item in items:
                    self.put_item_in_container(item, containers[0])

        # - drop -
        if tokens[0] == 'drop':
            if len(tokens) < 2:
                self.notify('Usage: drop item')
                return
            items = find_items_in_container(tokens[1], self.inventory())
            for item in items:
                self.drop_item(item)
            if not items:
                self.notify('You are not carrying a %s.' % tokens[1])
                return

        # - give -
        if tokens[0] == 'give':
            if len(tokens) < 3:
                self.notify('Usage: give item target')
                return
            items = find_items_in_container(tokens[1], self.inventory())
            if not items:
                self.notify("You are not carrying a %s" % tokens[1])
                return
            target = None
            for player in self.room.player_related.all():
                if tokens[2] in (player.id, player.name):
                    target = player
                    break
            if not target:
                self.notify("No-one by the name %s here." % tokens[2])
                return
            for item in items:
                self.give_item(item, target)

        # - kill -
        if tokens[0] == 'kill':
            if len(tokens) < 2:
                self.notify('Usage: kill target')
                return
            target = None
            for player in self.room.player_related.all():
                if tokens[1] in (player.id, player.name):
                    self.engage('player', player.id)
                    return
            for mob in self.room.mob_related.all():
                if tokens[1] in [mob.id] + mob.name.split(' '):
                    self.engage('mob', mob.id)
                    return

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
                # There are two saves here because the mob first loads in the
                # void and then is moved to the correct room so that players
                # do not see the wear messages
                mob = self.template_mob
                mob.id = None
                mob.room = Room.objects.get(pk=1)
                mob.template = False
                mob.save()

                self.spawned_mobs.add(mob)

                for attribute in ['armor', 'weapon', 'misc', 'sustenance']:
                    for base in getattr(self, attribute).all():
                        item = ItemInstance.objects.create(owner = mob,
                                                           base = base)

                mob.command('wear all')

                mob.hp = mob.max_hp
    
                mob.room = room
                mob.save()
                    
    
class Message(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now(),
                                   blank=False)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPES, blank=False)
    content = models.TextField(blank=False)
    destination = models.CharField(max_length=40, blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    author = generic.GenericForeignKey('content_type', 'object_id')
    
    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self.created = datetime.datetime.now()
    
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
        