import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from stark.apps.anima.constants import PLAYER_STATUSES, MESSAGE_TYPES, MOB_TYPES
from stark.apps.world.models import Room, RoomConnector, ItemInstance

MOVE_COST = 2 #TODO: move to global config

class Anima(models.Model):
    name = models.CharField(max_length=40) # should be unique for player subclass (not enforced @ db level)
    room = models.ForeignKey(Room, related_name="%(class)s_related")
    level = models.IntegerField(default=1)
    
    messages =  generic.GenericRelation('Message')
    
    hp = models.IntegerField(default=10)
    max_hp = models.IntegerField(default=10)
    
    mp = models.IntegerField(default=10)
    max_mp = models.IntegerField(default=10)
    
    sp = models.IntegerField(default=10)
    max_sp = models.IntegerField(default=10)
    
    main_hand = models.ForeignKey(ItemInstance, blank=True, null=True)
    
    target_type = models.ForeignKey(ContentType, blank=True, null=True)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = generic.GenericForeignKey('target_type', 'target_id')
    
    class Meta:
        abstract = True                

    def notify(self, msg):
        Message.objects.create(type='notification', destination=self.name, content=msg)
    
    def move(self, to_room=None, random=False):        
        if random:
            connector = RoomConnector.objects.filter(from_room=self.room).order_by('?')[0]
            to_room = connector.to_room
        elif to_room:
            connector = RoomConnector.objects.get(from_room=self.room, to_room=to_room)
        else:
            raise Exception('in Anima.move(), provide either a valid to_room or set random=True')

        # unless in builder mode, check for move points and deduct points
        if not (self.__class__.__name__ == 'Mob' or hasattr(self, 'builder_mode') and self.builder_mode == True):
            if self.mp < MOVE_COST:
                raise Exception("Not enough movement points to move.")
            else:
                self.mp -= MOVE_COST

        # save where the user was before the move
        from_room = self.room
        
        # move the user
        self.room = to_room

        # save
        self.save()
        
        # tell every player in the room the anima was in that it's gone
        for player in Player.objects.filter(room=from_room, status='logged_in'):
                Message.objects.create(
                    type = 'notification',
                    destination = player.name,
                    content = "%s leaves %s." % (self.name, connector.direction),
                )
        
        rev_direction = None
        if connector.direction == 'north': rev_direction = 'south'
        if connector.direction == 'east': rev_direction = 'west'
        if connector.direction == 'south': rev_direction = 'north'
        if connector.direction == 'west': rev_direction = 'east'
            
        # tell every player in the room the anima is moving to that it's,
        # arrived, or simply that it's moved if the observer is the one
        # performing the action
        for player in Player.objects.filter(room=to_room, status='logged_in'):
            if player == self:
                Message.objects.create(
                    type = 'notification',
                    destination = player.name,
                    content = "You leave %s" % connector.direction,
                )
            else:
                Message.objects.create(
                    type = 'notification',
                    destination = player.name,
                    content = "%s has arrived from the %s." % (self.name, rev_direction),
                )                
    
    def give_item(self, item, give_to):
        
        if item.owner.room != give_to.room:
            stark_log = logging.getLogger('StarkLogger')
            message = "%s can't give item %s to %s because they aren't in the same room" % (self.name, item.name, give_to.name)
            stark_log.debug(message)
            raise Exception(message)

        item.owner = give_to
        item.save()

        for player in self.room.player_related.all():
            if player == self:
                Message.objects.create(type='notification', destination=self.name, content="You give %s to %s." % (item.base.name, give_to.name))
            elif player == give_to:
                Message.objects.create(type='notification', destination=give_to.name, content="%s gives you %s." % (self.name, item.base.name))
            else:
                Message.objects.create(type='notification', destination=player.name, content="%s gives %s to %s" % (self.name, item.base.name, give_to.name))

    def drop_item(self, item):
        item.owner = self.room
        item.save()
        for player in self.room.player_related.all():
            if player == self:
                Message.objects.create(type='notification', destination=self.name, content="You drop %s." % item.base.name)
            else:
                Message.objects.create(type='notification', destination=player.name, content="%s drops %s." % (self.name, item.base.name))

    def get_item(self, item):
        if item.owner != self.room:
            stark_log = logging.getLogger('StarkLogger')
            message = "%s can't get item %s because they're in different rooms" % (self.name, item.name)
            stark_log.debug(message)
            raise Exception(message)

        item.owner = self
        item.save()
        
        for player in self.room.player_related.all():
            if player == self:
                Message.objects.create(type='notification', destination=self.name, content="You get %s." % item.base.name)
            else:
                Message.objects.create(type='notification', destination=player.name, content="%s gets %s." % (self.name, item.base.name))

    def get_item_from_container(self, item):
        # container is in player or in player's room
        if (item.owner.owner.__class__ is Room and item.owner.owner == self.room) or \
           (item.owner.owner.__class__ is Player and item.owner.owner == self):
                        
            for player in self.room.player_related.all():
                if player == self:
                    Message.objects.create(type='notification', destination=self.name, content="You get %s from %s." % (item.base.name, item.owner.base.name))
                else:
                    Message.objects.create(type='notification', destination=player.name, content="%s gets %s from %s." % (self.name, item.base.name, item.owner.base.name))

            item.owner = self
            item.save()

        else:
            stark_log = logging.getLogger('StarkLogger')
            message = "%s can't get item %s from container %s because they're in different rooms" % (self.name, item.name, item.owner.name)
            stark_log.debug(message)
            raise Exception(message)

    def put_item_in_container(self, item, container):
        # container is in the room
        if (container.owner.__class__ is Room and container.owner == item.owner.room) or \
           (container.owner.__class__ is Player and container.owner == item.owner):
            
                for player in self.room.player_related.all():
                    if player == self:
                        Message.objects.create(type='notification', destination=self.name, content="You put %s in %s." % (item.base.name, container.base.name))
                    else:
                        Message.objects.create(type='notification', destination=player.name, content="%s puts %s in %s." % (self.name, item.base.name, container.base.name))
            
                item.owner = container
                item.save()

        else:
            stark_log = logging.getLogger('StarkLogger')
            message = "%s can't put item %s in container %s because they're in different rooms" % (self.name, item.base.name, container.base.name)
            stark_log.debug(message)
            raise Exception(message)
        

    def engage(self, target_type, target_id):
        not_here = "No-one by that name."
        try:
            target = ContentType.objects.get(model=target_type).model_class().objects.get(pk=target_id)
            if self.room != target.room:
                self.notify(not_here)

            self.target = target
            self.save()
        except Exception:
            self.notify(not_here)

    def save(self, *args, **kwargs):
        if not hasattr(self, 'room'):
            try:
                room = Room.objects.get(pk=1)
                self.room = room
            except Room.DoesNotExist:
                raise Exception("There needs to be a Room object with pk = 1")
        super(Anima, self).save(*args, **kwargs)
        return self

    def __unicode__(self):
        return u"%s" % self.name

class Player(Anima):
    user = models.ForeignKey(User, related_name='players')
    builder_mode = models.BooleanField(default=False)
    temporary = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PLAYER_STATUSES)
    last_activity = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.last_activity = datetime.datetime.now()
        return super(Player, self).save(*args, **kwargs)

class Mob(Anima):
    # static mobs can't move
    static = models.BooleanField(default=False)

class Message(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now(), blank=False)
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