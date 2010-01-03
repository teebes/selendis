def find_items_in_container(keyword, container, find_container=False):
    """
    Find one or more items from a container.
    If find_container is passed as True, only the first found container will
    be returned in the list.
    """
    
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
