import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from stark.apps.world.models import Room, RoomConnector

#MOB_TYPES = (
#    ('humanoid','Humanoid'),
#    ('beast', 'Beast'),
#)

class Anima(models.Model):
    name = models.CharField(max_length=40) # should be unique for player subclass (not enforced @ db level)
    room = models.ForeignKey(Room, related_name="%(class)s_related")
    level = models.IntegerField(default=1)
    
    messages =  generic.GenericRelation('Message')
    
    hp = models.IntegerField(default=10)
    max_hp = models.IntegerField(default=10)
    
    mv = models.IntegerField(default=10)
    max_mv = models.IntegerField(default=10)
    
    sp = models.IntegerField(default=10)
    max_sp = models.IntegerField(default=10)
    
    class Meta:
        abstract = True                
    
    def move(self, to_room=None, random=False):
        if random:
            connector = RoomConnector.objects.filter(from_room=self.room).order_by('?')[0]
            to_room = connector.to_room
        elif to_room:
            connector = RoomConnector.objects.get(from_room=self.room, to_room=to_room)
        else:
            raise Exception('in Anima.move(), provide either a to_room or set random=True')

        from_room = self.room
        self.room = to_room
        self.save()
        
        # tell every player in the room the mob was in that it's gone
        for player in Player.objects.filter(room=from_room):
            Message.objects.create(
                type = 'notification',
                created = datetime.datetime.now(),
                destination = player.name,
                content = "%s leaves %s." % (self.name, connector.direction)
            )
        
        rev_direction = None
        if connector.direction == 'north': rev_direction = 'south'
        if connector.direction == 'east': rev_direction = 'west'
        if connector.direction == 'south': rev_direction = 'north'
        if connector.direction == 'west': rev_direction = 'east'
            
        # tell every player in the room the mob is moving to that it's arrived
        for player in Player.objects.filter(room=to_room):
            Message.objects.create(
                type = 'notification',
                created = datetime.datetime.now(),
                destination = player.name,
                content = "%s has arrived from the %s." % (self.name, rev_direction),
            )
    
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

PLAYER_STATUSES = (
    ('logged_in', 'Logged In'),
    ('logged_out', 'Logged Out'),
    ('guest', 'Guest'),
    ('inactive', 'Inactive'),
)

class Player(Anima):
    user = models.ForeignKey(User, related_name='players')
    builder_mode = models.BooleanField(default=False)
    temporary = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PLAYER_STATUSES)
    last_activity = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.last_activity = datetime.datetime.now()
        return super(Player, self).save(*args, **kwargs)

class Mob(Anima): pass

MESSAGE_TYPES = (
    ('chat', 'Chat'),
    ('clan', 'Clan'),
    ('direct', 'Direct'),
    ('notification', 'Notifiation'),
)

class Message(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now(), blank=False)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPES, blank=False)
    content = models.TextField(blank=False)
    destination = models.CharField(max_length=40, blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    author = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return u"%s: %s" % (self.author, self.content)