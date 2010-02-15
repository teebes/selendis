import datetime
import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class EmailConfirmation(models.Model):
    """Generic e-mail confirmation object"""
    user = models.ForeignKey(User)
    key = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u"%s:%s" % (self.email, self.key)
        
class Preferences(models.Model):
    """The account-wide preferences"""
    # NB: any field here that does not have a default value should be
    # reflected in the creation signal
    
    user = models.OneToOneField(User, related_name='preferences')
    
    map_height = models.IntegerField(default=11)
    map_width = models.IntegerField(default=11)
    
    log_memory = models.IntegerField(default=30)

    # log_memory
    # echo_ui_cmds_to_log
    # chat preferences

def post_account_creation(*args, **kwargs):
    if kwargs['created']:
        Preferences.objects.create(user=kwargs['instance'])

post_save.connect(post_account_creation, sender=User)