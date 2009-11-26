#!/usr/bin/env python
if __name__ == "__main__":
    from django.core.management import setup_environ
    from stark import settings
    setup_environ(settings)

    import datetime
    import logging
    import time
    import random

    from django.db import transaction

    from stark.apps.anima.models import Mob, Player, Message
    from stark.apps.world.models import RoomConnector

    # base event class
    class PeriodicEvent(object):
        def __init__(self, interval):
            self.interval = interval
            self.last_executed = None
        
        def should_execute(self):
            if not self.last_executed or datetime.timedelta(seconds=self.interval) < datetime.datetime.now() - self.last_executed:
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
        def execute(self):
            super(Tick, self).execute()
            
            # move mobs
            for mob in Mob.objects.filter(static=False):
                if random.randint(0, 10) == 0:
                    print 'moving %s' % mob.name
                    mob.move(random=True)
                    
            # TODO: make the regen amount a configurable value
            # give each logged in players moves, if they're not at max
            TICK_MP_REGEN_RATE = 20
            for player in Player.objects.filter(status='logged_in').extra(where=['mp < max_mp']):
                player.mp += TICK_MP_REGEN_RATE
                if player.mp > player.max_mp:
                    player.mp = player.max_mp
                player.save()
            
            pulse_log = logging.getLogger('PulseLogger')
            pulse_log.debug('tick @ %s' % self.last_executed)
            
            return
        
    class CleanUp(PeriodicEvent):
        def execute(self):
            super(CleanUp, self).execute()
            
            # cleanup notifications
            count = 0
            for message in Message.objects.filter(type='notification', created__lte=(datetime.datetime.now() - datetime.timedelta(minutes=10))):
                message.delete()
                count += 1
                
            self.log('deleted %s messages' % count)
                
    events = [
        Tick(10),
        CleanUp(30),
    ]
    
    # pulse loop
    while(True):
        time.sleep(2)
        
        pulse_log = logging.getLogger('PulseLogger')
        pulse_log.debug("pulse @ %s" % datetime.datetime.now())
        
        for event in events:
            if event.should_execute():
                event.execute()

