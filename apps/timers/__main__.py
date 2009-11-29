#!/usr/bin/env python
if __name__ == "__main__":
    from django.core.management import setup_environ
    from stark import settings
    setup_environ(settings)

    import time

    from stark.apps.timers.events import Tick, CleanUp

    events = [
        Tick(10),
        CleanUp(30),
    ]
    
    # pulse loop
    while(True):
        time.sleep(2)
        
        for event in events:
            if event.should_execute():
                event.execute()

