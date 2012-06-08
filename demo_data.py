from models import default_conn

from models import Character
from models import Room
from models import Item
from models import item_assignments

def rooms():
    room, created = Room.update_or_create(1, {
        "name": "Heart of the World",
        "description": "The very center of the world",
        "x": 0,
        "y": 0,
        "z": 0,
        "items": [],
        "north": 2,
    })

    room, created = Room.update_or_create(2, {
        "name": "North of the heart",
        "description": "A short ways north of the center of the world",
        "x": 0,
        "y": 1,
        "z": 0,
        "items": [],
        "south": 1,
    })

def items():
    item, created = Item.update_or_create(1, {
        "type": "weapon",
        "name": "A flaming crystal sword",
        "weight": 1,
        "durability": 100,
    })

    teebes = Character.get('teebes')
    teebes.room.receive_item(1)
    print teebes.room.inventory
    print teebes.get_item('1')


if __name__ == "__main__":
    rooms()
    items()

