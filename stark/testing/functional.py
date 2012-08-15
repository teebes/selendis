from stark.models import Anima
from stark.models import Room

rooms = [
    {
        "key": "room1",
        "name": "Center of the World",
        "x": 0,
        "y": 0,
        "z": 0,
        "north": { "key": "room2" },
    },
    {
        "key": "room2",
        "name": "North of the World",
        "x": 0,
        "y": 0,
        "z": 0,
        "south": { "key": "room1" }
    }
]

[ Room(room) for room in rooms ]

cat = Anima({
    "key": "cat",
    "name": "a cat",
    "stats": { "mp": 200 },
    "room": { "key": "room1" }
})

dog = Anima({
    "key": "dog",
    "name": "a dog",
    "stats": { "mp": 200 },
    "room": { "key": "room1" }
})

print cat.room.name
cat.move('north')
print cat.room.name


