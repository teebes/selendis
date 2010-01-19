import datetime
import logging
import time
import random

from django.db import transaction

from stark import config
from stark.apps.anima.models import Mob, MobLoader, Player, Message
from stark.apps.world.models import RoomConnector, Room, ItemInstance

# base event class
class PeriodicEvent(object):
    def __init__(self, interval):
        self.interval = interval
        self.last_executed = None
    
    def should_execute(self):
        if not self.last_executed or \
           datetime.timedelta(seconds=self.interval) < datetime.datetime.now() - self.last_executed:
            return True
        return False

    def log(self, msg):
        pulse_log = logging.getLogger('PulseLogger')
        pulse_log.debug(msg)

    def execute(self):
        self.last_executed = datetime.datetime.now()
        return

# the longer ticks which handle regen & repops
class Tick(PeriodicEvent):
    
    @transaction.commit_on_success
    def move_mobs(self):
        # move mobs
        for mob in Mob.objects.exclude(static=True).exclude(template=True):
            if random.randint(0, 10) == 0:
                mob.move(random=True)
            
    @transaction.commit_on_success
    def regen(self):
        TICK_HP_REGEN_RATE = getattr(config, 'TICK_HP_REGEN_RATE', 4)
        TICK_MP_REGEN_RATE = getattr(config, 'TICK_MP_REGEN_RATE', 20)
        
        # players regen moves
        for player in Player.objects.filter(status='logged_in').extra(where=['mp < max_mp']):
            player.regen('mp', TICK_MP_REGEN_RATE)
            
        # players regen health
        for player in Player.objects.filter(status='logged_in').extra(where=['hp < max_hp']):
            player.regen('hp', TICK_HP_REGEN_RATE)

    def execute(self):
        super(Tick, self).execute()
        
        # mob loaders
        for loader in MobLoader.objects.all():
            loader.run()
        
        self.move_mobs()
        self.regen()
        
        self.log('tick @ %s' % self.last_executed)
        
        return

class Combat(PeriodicEvent):
    
    @transaction.commit_on_success
    def combat_round(self):
        for player in Player.objects.filter(status='logged_in',
                                            target_type__isnull=False):
            player.combat_round()

        for mob in Mob.objects.filter(target_type__isnull=False):
            mob.combat_round()
    
    def execute(self):
        super(Combat, self).execute()
        self.combat_round()
        return

class CleanUp(PeriodicEvent):
    
    @transaction.commit_on_success
    def cleanup_messages(self):
        msg_life = getattr(config, 'MESSAGE_LIFESPAN', 10)
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(minutes=msg_life)
        for message in Message.objects.filter(
            type='notification',
            created__lte=(datetime.datetime.now() - datetime.timedelta(minutes=10))):
            message.delete()

    def cleanup_corpses(self):
        decay = getattr(config, 'CORPSE_DECAY_LENGTH', 5)
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(seconds=60 * decay)
        for item in ItemInstance.objects\
                        .filter(name__startswith='the corpse of')\
                        .filter(modified__lt=threshold):
            if item.owner.__class__ == Room:
                item.owner.notify('%s decays into a pile of dust.' % item.name)
                item.delete()
    
    def cleanup_temporary_players(self):
        temp_life = getattr(config, 'TEMPORARY_PLAYER_LIFESPAN', 1)
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(days=temp_life)
        temp_players = Player.objects.filter(temporary=True,
                                             last_activity__lt=threshold)
        temp_users = map(lambda x: x.user, temp_players)

        for player in temp_players.all():
            player.room.notify('%s fades from existence.' % player.name)

        # delete the characters
        temp_players.delete()

        # delete the temporary users
        for user in temp_users:
            user.delete()
    
    def execute(self):
        super(CleanUp, self).execute()
        
        self.cleanup_messages()
        self.cleanup_corpses()
        self.cleanup_temporary_players()
        return