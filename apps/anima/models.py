from django.contrib.auth.models import User
from django.db import models

from stark.apps.world.models import Room

class Anima(models.Model):
    name = models.CharField(max_length=40, unique=True)
    room = models.ForeignKey(Room, related_name="%(class)s_related")
    
    class Meta:
        abstract = True    
    
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
    user = models.ForeignKey(User)
    level = models.IntegerField(default=1)
    builder_mode = models.BooleanField(default=False)

class Mob(Anima): pass