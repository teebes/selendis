from django.db import models

from stark.apps.anima.models import Player

class Alias(models.Model):
    name = models.CharField(max_length=40)
    command = models.CharField(max_length=100)
    player = models.ForeignKey(Player, related_name='aliases')
