import datetime
import hashlib

from django.contrib.auth.models import User
from django.db import models

class EmailConfirmation(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u"%s:%s" % (self.email, self.key)