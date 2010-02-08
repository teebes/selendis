from decimal import Decimal

from stark.apps.world.models import Room, RoomConnector, ItemInstance

def rev_direction(direction):
    if direction == 'north':
        return 'south'
    elif direction == 'east':
        return 'west'
    elif direction == 'south':
        return 'north'
    elif direction == 'west':
        return 'east'
    else:
        raise Exception('Invalid direction: %s' % direction)

def get_container_weight(container):
    weight = Decimal('0.00')
    for item in ItemInstance.objects.owned_by(container):
        weight += item.total_weight()
    return weight

def can_hold_item(carrier, item):
    free_room = carrier.capacity - get_container_weight(carrier)
    return free_room > item.total_weight()

def find_items_in_container(keyword, container, find_container=False):
    """
    Find one or more items from a container.
    If find_container is passed as True, only the first found container will
    be returned in the list.
    """

    # make sure the items are containers, i.e. with a non-null capacity
    if find_container == True:
        container = filter(lambda x: x.base.capacity > 0, container)
        # TODO: since when getting a container we only want one container,
        # how do we make sure the 'all' doesn't work below?
    
    if keyword == 'all':
        return container
    
    items = []
    for item in container:
        # try the ID
        if keyword == str(item.id):
            return [item]
        
        # try the words in the item's name
        item_words = item.base.name.split(' ')
        if keyword in item_words:
            return [item]

    return items

def draw_map(x, y, width=5, height=0):
    if not height:
        height = width
    
    x_range = (x - int(round(width/2)),
               x + int(round(width/2)))
    y_range = (y - int(round(height/2)),
               y + int(round(height/2)))
    
    map = {}
    
    for room in Room.objects.filter(xpos__range=x_range,
                                    ypos__range=y_range):
        room_dict = {
            'xpos': room.xpos,
            'ypos': room.ypos,
            'type': room.type,
        }
        for connection in room.from_room.all():
            room_dict[connection.direction] = connection.type

        map[room.id] = room_dict
    
    map['x'] = x
    map['y'] = y
    map['width'] = width
    map['height'] = height
    
    return map