from stark.apps.world.models import RoomConnector

def direct_connectors():
    for connector in RoomConnector.objects.all():
        if connector.from_room.xpos == connector.to_room.xpos and connector.from_room.ypos - 1 == connector.to_room.ypos:
            connector.direction = 'north'
        if connector.from_room.xpos + 1 == connector.to_room.xpos and connector.from_room.ypos == connector.to_room.ypos:
            connector.direction = 'east'
        if connector.from_room.xpos == connector.to_room.xpos and connector.from_room.ypos + 1 == connector.to_room.ypos:
            connector.direction = 'south'
        if connector.from_room.xpos - 1 == connector.to_room.xpos and connector.from_room.ypos == connector.to_room.ypos:
            connector.direction = 'west'
            
        connector.save()
        
    print 'done'