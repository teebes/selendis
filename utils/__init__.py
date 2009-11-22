from stark.apps.anima.models import Mob, Player
from stark.apps.world.models import Room, RoomConnector

def generate_mobs(mobs_per_batch=5):
    # creates a batch of mobs
    mob_names = ['a small black cat', 'a black dog', 'a cute brown deer', 'a zombie', 'a peasant']
    
    for i in range(0, mobs_per_batch):
        for mob_name in mob_names:
            room = Room.objects.exclude(type='water').order_by('?')[0]
            
            mob = Mob()
            mob.name = mob_name
            mob.room = room
            mob.save()
            
def move_mobs():
    # moves all mobs by one room in a direction they can go
    for mob in Mob.objects.all():
        connector = RoomConnector.objects.filter(from_room=mob.room).order_by('?')[0]
        mob.room = connector.to_room
        mob.save()
