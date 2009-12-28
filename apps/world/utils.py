def find_items_in_container(keyword, container):
    items = []
    for item in container:
        item_words = item.base.name.split(' ')
        if keyword == 'all' or \
           keyword == item.id or \
           keyword in item_words:
            items.append(item)
    return items
