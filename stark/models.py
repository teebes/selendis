import copy
import inspect
import json
import logging
import sys

from stark import config 
from stark.core.exceptions import WrongDirectionError
from stark.core.exceptions import ExhaustedError
from stark.core.rjson import RJSON

LOG_LEVEL = 'debug'
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
console = logging.StreamHandler()
console.setLevel(getattr(logging, LOG_LEVEL.upper()))
logger.addHandler(console)

DIRECTIONS = ['north', 'east', 'south', 'west', 'up', 'down']
TERMINAL = 'terminal'

class Room(RJSON):
    """
    A physical location in the world, with unique (x, y, z)
    coordinates and the ability to connect to other rooms.

    Acts as a container for Anima and Items.

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

    def get_direction(self, direction):
        """
        Return the Room instance that one moves to by following a direction.
        """

        assert(direction in DIRECTIONS)
        return getattr(self, direction, None)

    def get_exits(self):
        """
        Return the exits from a Room

        Sample return value::

            ['N', 'E', 'W']
        """

        exits = [
            direction[0].upper()
            for direction in DIRECTIONS
            if hasattr(self, direction)
        ]

        return exits

    def get_rendering_context(self):
        """
        Returns a context to be used by a front-end to render
        the room.
        """
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

from stark.data import load_world
class Anima(RJSON):
    """
    >>> load_world.load_demo_rooms()
    >>> anima = Anima({
    ...     'key': 'anima', 
    ...     'room': { 'key': 'center' }, 
    ...     'stats': {
    ...         'mp': 200
    ...     }
    ... })
    >>> anima.room.name
    'Center'
    >>>
    """

    #: The room in which the Anima instance is in.
    room = Room

    #: The stats of the Anima instance.
    stats = { 'mp': 200 }

    def move(self, direction):
        """
        Move in a direction, changing the anima's room 
        attribute to the destination Room if the move
        if allowed.

        Has the side effect of lowering an Anima's movement points.

        :returns: :class:`models.Room`

        >>> anima = load_world.load_demo_anima()
        >>> anima.room.name
        'Center'
        >>> 'N' in anima.room.get_exits()
        True
        >>> anima.move('north') # doctest:+ELLIPSIS
        <Room - ...
        >>> anima.room.name
        'North'
        >>> anima.room.get_exits()
        ['S']
        >>> anima.move('north') # doctest:+IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        WrongDirectionError: ...
        """

        dest = self.room.get_direction(direction)
        if dest is None:
            raise WrongDirectionError(direction)

        if self.stats.mp < config.MOVEMENT_COST:
            raise ExhaustedError(self.stats.mp)

        self.room = dest
        self.stats.mp -= config.MOVEMENT_COST

        return dest


