import copy
import inspect
import json
import logging
import sys

from stark.core.rjson import Registry
from stark.core.rjson import Model

LOG_LEVEL = 'debug'
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
console = logging.StreamHandler()
console.setLevel(getattr(logging, LOG_LEVEL.upper()))
logger.addHandler(console)

DIRECTIONS = ['north', 'east', 'south', 'west', 'up', 'down']
TERMINAL = 'terminal'

class Room(Model):
    """
    >>> center = Room({ 
    ...     "x": 0, "y": 0, "z": 0, 
    ...     "key": "center", 
    ...     "name": "Center", 
    ...     "north": { 
    ...         "key": "north" 
    ...     }
    ... })
    >>> center.get_exits()
    ['N']

    >>> north = Room({ 
    ...     "x": 0, "y": 1, "z": 0, 
    ...     "key": "north", 
    ...     "name": "North",
    ...     "description": "There is little to see here.",
    ...     "south": { 
    ...         "key": "center",
    ...      }
    ...  })
    >>> north.get_exits()
    ['S']

    >>> print north.get_direction('south').name
    Center

    >>> north.get_direction('east') is None
    True

    >>> north.get_rendering_context() == {
    ...     'name': u'North',
    ...     'description': u'There is little to see here.',
    ...     'exits': ['S'],
    ... }
    True
    """

    x = 0
    y = 0
    z = 0
    name = "Untitled Room"

    # optional keys: DIRECTIONS

    def __call__(self):
        return [    
            self.name,
            self.exits,
        ]

    # because book.author.father.address.state
    # looks cleaner than
    # book['author']['father']['address']['state']

    def get_direction(self, direction):
        """
        Return the Room instance that one moves to by following a direction.
        """

        assert(direction in DIRECTIONS)
        return getattr(self, direction, None)

    def get_exits(self):
        "return the exits from a Room"

        exits = [
            direction[0].upper()
            for direction in DIRECTIONS
            if hasattr(self, direction)
        ]

        return exits

    def get_rendering_context(self):
        # TODO: unicode calls belongs elsewhere, probably Model.__init__ring_context(self):
        return {
            k: v 
            for k, v in { 
                "name": unicode(self.name),
                "description": unicode(getattr(self, 'description', None)),
                "exits": self.get_exits()
            }.items()
            if v is not None
        }

class Anima(Model):
    """
    >>> orig = Room({'key': 'orig', 'x': 0, 'y': 1, 'z': 0, 'name': 'Orig', 'south': {'key': 'dest'}})
    >>> dest = Room({'key': 'dest', 'x': 0, 'y': 0, 'z': 0, 'name': 'Dest', 'north': {'key': 'orig'}})
    >>> orig.south.key
    'dest'
    >>> anima = Anima({'key': 'anima', 'room': { 'key': 'orig' } })
    >>> anima.room.key
    'orig'
    >>> anima.move('south')
    >>> anima.room.key
    'dest'
    """

    room = Room

    def move(self, direction):
        dest = self.room.get_direction(direction)
        if dest:
            self.room = dest

    def goto(self, direction): pass
    def look(self, direction): pass
    

class Item(Model):
    """
    Fundamental assumption: the templates must be loaded first

    >>> ItemTemplate({
    ...     "key": "itemtemplate.1",
    ...     "name": "an apple",
    ...     "contains": False
    ... })
    >>> ItemTemplate({
    ...     "key": "itemtemplate.2",
    ...     "name": "a bag",
    ...     "contains": False
    ... })
    >>> bag = Item({
    ...     "key": "item.1",
    ...     "template": "itemtemplate.1"
    ... })
    >>> apple = Item({
    ...     "key": "item.2",
    ...     "template": "itemtemplate.2",
    ...     "contains": ["item.1"]
    >>> bag.contains
    [<Item 2 - a leather bag>]
    """

    key = None
    template = None

    def __init__(self, data):
        super(Item, self).__init__(data)

        # load the template
        self.template = Template.load(data['template'])

        if self.template.contains and not self.contains:
            self.contains = self.template.contains

class Base(Model): pass

class ItemTemplate(Base): pass

class Item(Base): pass

class World(Item):
    name = "The world"
    rooms = []
    items = []

def get_user_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return [item
            for item in inspect.getmembers(cls)
            if item[0] not in boring]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

