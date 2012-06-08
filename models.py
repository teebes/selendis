import copy
import inspect
import json
import logging
import redis
import sys

LOG_LEVEL = 'debug'
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
console = logging.StreamHandler()
console.setLevel(getattr(logging, LOG_LEVEL.upper()))
logger.addHandler(console)


default_conn = redis.Redis(db=1)

class Model(object):
    "Base class for all models"

    conn = default_conn

    key = None

    schema = {}

    def __init__(self, key, data={}):
        self.key = str(key)
        self.data = data
        for k, v in data.items():
            setattr(self, k, v)

    """
    def __getattribute__(self, attr): 
        try:
            return super(Model, self).__getattribute__(attr)
        except AttributeError:
            return None
    """

    def __setattr__(self, attr, value):
        super(Model, self).__setattr__(attr, value)
        if getattr(self, 'data', None) is None:
            self.data = {}
        elif attr != 'data':
            self.data[attr] = value

    def __repr__(self):
        return u"{model}: {key}".format(
            model=self.__class__.__name__,
            key=self.key,
        )

    @classmethod
    def get_packed_key(cl, key):
        key = str(key).lower()

        packed_key = '{model}-{key}'.format(
            model=cl.__name__.lower(),
            key=key,
        )
        return packed_key

    @classmethod
    def create(cl, key, data={}):
        packed_key = cl.get_packed_key(key)
        cl.conn.set(packed_key, json.dumps(data))
        return cl(key, data)
 
    @classmethod
    def get(cl, key):
        packed_key = cl.get_packed_key(key)
        data = cl.conn.get(packed_key)
        if data is None:
            return None
        c = cl(key, json.loads(data))
        return cl(key, json.loads(data))

    @classmethod
    def get_or_create(cl, key, data={}):
        instance = cl.get(key)
        created = False
        if instance is None:
            instance = cl.create(key, data)
            created = True
        return instance, created

    @classmethod
    def update_or_create(cl, key, data={}):
        instance, created = cl.get_or_create(key, data)
        if not created:
            instance.data = data
            instance.save()
        return instance, created

    @property
    def packed_key(self):
        return self.__class__.get_packed_key(self.key)
     
    def check_id(self):
        # checks that the model has a valid ID
        if id is None:
            raise ValueError('Model instance has no ID')

    def save(self, data=None):
        self.conn.set(self.packed_key, json.dumps(self.data))
        return self

    @classmethod
    def sync(cl):
        cl_name = cl.__name__.lower()

        if hasattr(cl, 'schema'):
            logger.debug('Processing "{0}"...'.format(cl_name))
            keys = cl.conn.keys('{0}-*'.format(cl_name))
            for key in keys:
                data = json.loads(cl.conn.get(key))
                for attr, default in cl.schema.items():
                    if data.get(attr) is None:
                        data[attr] = default
                cl.conn.set(key, json.dumps(data))
                logger.debug('\tProcessed "{0}".'.format(key))


class ItemContainerMixin(object):
    def __init__(*args, **kwargs):
        super(ItemContainerMixin, self).__init__(*args, **kwargs)
        self.schema['items'] = [] 

    @property
    def inventory(self):
        return [
            Item.get(key) for key in self.items
        ]

    def receive_item(self, item_id):
        # record the new item ownership in the m2m table
        default_conn.hset('item_assignments', item_id, self.packed_key)

        _items = set(self.items)
        _items.add(item_id)
        self.items = list(_items)
        self.save()


class Character(Model, ItemContainerMixin):
    """
    Pack: charcter-{id}
    """

    online = {}

    schema = {
        'exp': 1,
        'hp': 100,
        'items': [],
        'level': 1,
        'max_hp': 100,
        'room_id': 1,
    }

    @classmethod
    def broadcast(cl, msg, only=None, exclude=None):
        _online = copy.copy(cl.online)

        if only is not None:
            _online = {
                key: handler 
                for key, handler in _online.items()
                    if key in only
            }

        if exclude is not None:
            _online = {
                key: handler 
                for key, handler in _online.items()
                if key not in exclude
            }

        for handler in _online.values():
            handler.to_client(msg)

        return [msg, _online.keys()]

    @property
    def room(self):
        return Room.get(self.room_id)

    def get_item(self, keyword):
        # pick up an item from a room in which the character should be

        # get the possible items that can be picked up in this room
        items_in_room = self.room.inventory

        picked_up_items = []

        if keyword.lower() == 'all':
            for item in items_in_room:
                self.receive_item(item.key)
                picked_up_items.append(item.name)

        else:
            keyword_tokens = keyword.split(' ')
            for keyword_token in keyword_tokens:
                for item in items_in_room:
                    for item_token in item.name.split(' '):
                        if keyword_token in item_token:
                            self.receive_item(item.key)
                            picked_up_items.append(item.name)

        to_char = ""
        to_room = ""
        for item_name in picked_up_items:
            to_char += "You get {0}.".format(item_name)
            to_room += "{0} gets {1}.".format(self.name, item_name)

        return to_char

        if to_char:
            self.to_client(to_char)
            self.room.broadcast(to_room, exclude=[self.key])

        return picked_up_items

    def move(self, direction):
        dest_id = getattr(self.room, direction, None)

        if dest_id is None:
            return "You cannot go that way."
        else:
            self.room_id = dest_id
            self.save()
            return "You leave {dir}.".format(dir=direction)

    def to_client(self, msg):
        return online[self.key].to_client(msg)


class Item(Model):
    schema = {
        'durability': 100,
        'name': 'Untitled Item',
        'type': 'misc',
        'weight': 1,
    }

    @property
    def owner(self):
        # check that the item is in the character's room
        item_owner = default_conn.hget('item_assignments', self.key)
        if item_owner is None:
            raise ValueError("Item ID {0} has no owner".format(item_id))

        # unpack the key
        model, key = item_owner.split('-')
        # cap first the model name
        _model = model[0].upper() + model[1:]
        return globals()[_model].get(key)

    def __repr__(self):
        return u"{0} - {1}".format(super(Item, self).__repr__(), self.name)


class Player(Model):
    name = "New Player"


class Room(Model, ItemContainerMixin):
    directions = [
        'north',
        'east',
        'south',
        'west',
        'up',
        'down',
    ]

    def __repr__(self):
        return u"{super_repr} - {name}".format(
            super_repr = super(Room, self).__repr__(),
            name = self.name,
        )

    @property
    def present_chars(self):
        chars = [
            key
            for key, handler in Character.online.items()
            if handler.char.room.key == self.key
        ]
        return chars

    @property
    def obvious_exits(self):
        exits = []
        for direction in self.directions:
            if getattr(self, direction, None) is not None:
                exits += direction[0].upper()
        return ' '.join(exits)

    def broadcast(self, msg, exclude=[]):
        chars = [ char for char in self.present_chars if char not in exclude ]
        return Character.broadcast(msg, only=chars)

    def render(self, pov_char=None):
        # room name / title
        out = "{name}\n"

        # room description
        out += "{desc}\n"

        # exits
        out += "[ obvious exits: {exits} ]\n"

        # who else is in the room
        for char in self.present_chars:
            if char != pov_char:
                out += "{char} is here.\n".format(char=char)
        

        out = out.format(
            name=self.name,
            exits=self.obvious_exits,
            desc=self.description,
        )
        return out

def item_assignments(item_id=None):
    return default_conn.hgetall('item_assignments')


def test():
    teebes = Character.get('teebes')
    print teebes.room
    
if __name__ == "__main__":
    if len(sys.argv) > 1:

        if sys.argv[1] == 'test': 
            test()

        elif sys.argv[1] == 'sync':
            models = { 
                k.lower(): v
                for k, v in globals().items()
                if inspect.isclass(v) 
            }
            if len(sys.argv) > 2:
                models[sys.argv[2]].sync()
            else:
                for model in models.values():
                    model.sync()

            


