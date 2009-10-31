from django.db import models

class Room(models.Model):
    xpos = models.IntegerField(blank=False)
    ypos = models.IntegerField(blank=False)
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField()
    
    def __unicode__(self):
        return u"%s, %s: %s" % (self.xpos, self.ypos, self.title)
        
    connected_rooms = models.ManyToManyField('self', through='RoomConnector', symmetrical=False)

CONNECTOR_TYPES = [
    ('Normal', 'Normal'),
]
    
class RoomConnector(models.Model):
    from_room = models.ForeignKey('Room', related_name='from_room')
    to_room = models.ForeignKey('Room', related_name='to_room')
    type = models.CharField(max_length=40, choices=CONNECTOR_TYPES)

"""
class mytest(models.Model):
     parents=models.ManyToManyField('self', through='parents', symmetrical=False)

class parents(models.Model):
     mytest=models.ForeignKey('mytest', related_name='original')
     parent=models.ForeignKey('mytest', related_name='parent')
"""