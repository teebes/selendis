import json
import sys
import unittest

#from mock import Mock

#from websocket import create_connection
#import websocket

from stark.models import Model
from stark.core.models import registry
from stark.models import Room

class TestCase(unittest.TestCase):
    def tearDown(self):
        registry.reset()


class ModelTestCase(TestCase):
    def test_data_is_required(self):
        with self.assertRaises(TypeError): Model()

    def test_key_is_required(self):
        with self.assertRaises(KeyError): Model({})

    def test_load_simple_model(self):
        data = {  'key': 'a_key', 'foo': 'bar' }
        instance = Model(data)
    
        # basic processing
        self.assertEqual(instance.key, 'a_key')
        self.assertEqual(instance.foo, 'bar')
        self.assertEqual(instance._data, data)

    def test_nested(self):
        data = { "key": "outer_key", "inner": { "key": "inner_key" } }
        instance = Model(data)
        self.assertEqual(instance.inner.key, 'inner_key')

    def test_relation(self):
        data1 = { "key": "john", "age": 46 }
        data2 = { "key": "mybook", "author": { "key": "john" } }
        instance = Model(data1)
        instance = Model(data2)
        self.assertEqual(instance.author.age, 46)


        # TODO: review below in a bit and see if that should be added
        # key is not `modeltype-key` format, therefore this doesn't get added
        # to the registry
        #self.assertEqual(registry.instances.get('mykey'), None)

class PlayerInRoom(TestCase):
    def test_move_north(self):
        start_room = Room({
            "key": "start_room",
            "x": 0,
            "y": 0,
            "z": 0,
            "name": "Start Room",
            "north": "end_room",
        })
        start_room = Room({
            "key": "end_room",
            "x": 0,
            "y": 1,
            "z": 0,
            "name": "End Room",
            "south": "start_room",
        })
        
        
        #player_room = Player({
        #    "key": "player",
        #    "
        #})


if __name__ == "__main__":
    unittest.main()


