from stark.apps.world.models import ItemInstance

def find_items_in_container(keyword, container):
    items = []
    for item in container:
        item_words = item.split(' ')
        if keyword == 'all' or \
           keyword == item.id or \
           keyword in item_words:
            items.append(item)
    return items
        

def parse_command(cmd, anima):
    tokens = map(lambda x: x.lower(), cmd.split(' '))

    #if tokens[1] == 'get':
    #    player_inventory = ItemInstance.objects.get(owner=)
