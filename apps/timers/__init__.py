import threading

from stark.apps.timers.events import CleanUp, Combat, Tick

PULSE_INTERVAL = 2 # seconds

events = [
    Combat(1),
    Tick(10),
    CleanUp(30),
]

def check_pulse():
    """
    Checks to see if a pulse thread is running, and if not launches one in
    daemon mode
    """
    no_pulse = True
    for thread in threading.enumerate():
        if thread.name == 'stark_pulse_thread':
            no_pulse = False
            break

    if no_pulse:
        t = threading.Thread(target=pulse)
        t.name = 'stark_pulse_thread'
        t.deamon = True
        t.start()
        print 'starting pulse thread'

def pulse():
    for event in events:
        if event.should_execute():
            event.execute()
    t = threading.Timer(PULSE_INTERVAL, pulse)
    t.name = 'stark_pulse_thread'
    t.start()
    