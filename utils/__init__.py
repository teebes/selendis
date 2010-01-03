import random

from django.contrib.contenttypes.models import ContentType

from stark.apps.world.models import Room, RoomConnector, ItemInstance, Misc

def roll_percent(threshold):
    if threshold >= random.randint(1, 100):
        return True
    else:
        return False

def cleanup_corpses():
    count = 0
    for corpse in Misc.objects.filter(name__startswith='The corpse of'):
        corpse_type = ContentType.objects.get_for_model(corpse)
        corpse_instance = ItemInstance.objects.filter(base_type__pk=corpse_type.id, base_id=corpse.id).delete()
        corpse.delete()
        count += 1

    print 'deleted %s corpses' % count
