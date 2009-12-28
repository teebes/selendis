def find_items_in_container(keyword, container):
    if keyword == 'all':
        return container
    
    items = []
    for item in container:
        item_words = item.base.name.split(' ')
        if keyword == item.id or \
           keyword in item_words:
            return [item]

    return items
