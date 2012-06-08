import json
import sys
import unittest

from mock import Mock

from websocket import create_connection
import websocket

from stark.models import Model


class TestModel(Model): conn = Mock()

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        TestModel.conn = Mock()

    def test_model_instantiation(self):
        # models must have keys
        self.assertRaises(TypeError, TestModel)

        # provided key is available on the instance
        self.assertEqual(TestModel('key').key, 'key')

        instance = TestModel('key', data={ 'foo': 'bar' })

        # passed data can be accessed via attribute
        self.assertEqual(instance.foo, 'bar')

        # passed data is saved in .data
        self.assertEqual(instance.data['foo'], 'bar')

        # attribute that does not exist returns None
        self.assertEqual(instance.dne, None)

        # setting a new attribute updates self.data
        instance.x = 'y'
        self.assertEqual(instance.data['x'], 'y')

    def test_key_packing(self):
        # test class method's packed key fetching
        self.assertEqual(
            TestModel.get_packed_key('key'),
            'testmodel-key'
        )

        # instance key packing
        instance = TestModel('key')
        self.assertEqual(instance.packed_key, 'testmodel-key')

    def test_db_creation(self):
        instance = TestModel.create('key', data={'foo': 'bar'})
        self.assertEqual(instance.key, 'key')
        self.assertEqual(instance.foo, 'bar')

    def test_db_get(self):
        TestModel.conn.get = lambda x: '{ "foo": "bar" }'
        instance = TestModel.get('key')
        self.assertEqual(instance.key, 'key')
        self.assertEqual(instance.foo, 'bar')

    def test_get_or_create(self):

        """
        # get
        TestModel.conn.get = lambda x: '{ "foo": "bar" }'
        instance, created = TestModel.get_or_create('key', { "foo": "bar" })
        self.assertEqual(created, False)
        self.assertEqual(instance.key, 'key')
        self.assertEqual(instance.foo, 'bar')
        """

        # create
        TestModel.conn.get = lambda x: None
        #TestModel.conn.create = lambda x: '{ "foo": "bar" }'
        instance, created = TestModel.get_or_create('key', { "foo": "bar" })
        self.assertEqual(created, True)
        self.assertEqual(instance.key, 'key')
        self.assertEqual(instance.foo, 'bar')
    """
    def test_update_or_create(self):
        # update 
        TestModel.conn.get = lambda x: None
        #TestConn.
        pass
"""


host_string = '0.0.0.0:8888'

script = [
    [ # try to login with non existing character
        u"doesnotexist",
        { 
            u"context": u"authentication.query_char_creation",
            u"message": u"Create character 'doesnotexist'?"
        }
    ],
    [ # choose not to create new character
        u"n",
        { 
            u"context": u"authentication.get_charname",
            u"message": u"Enter your character name:", 
        },
    ],
    [ # successful login
        u"teebes",
        {
            u"context": u"default",
            u"message": u"Welcome, teebes.",
        }
    ],
]

#[ # try to login with non existing character
#    u"teebes",
#    {
#        u"context": u"authentication.query_char_creation",
#        u"message": u"Create character 'teebes'?",
#    }
#],
#[
#    u"y",
#    {
#        u"context": u"default",
#        u"message": u"Welcome, teebes.",
#    }
#],
 
VERBOSE = False

def on_message(ws, message):
    message = json.loads(message)

    if VERBOSE:
        print 'Received:'
        print json.dumps(message, indent=4)
        print '----'

    if ws.expected_output is not None:
        if message == ws.expected_output:
            print 'OK'
        else:
            feedback = 'Expected:\n\t"{0}"\n'.format(ws.expected_output)
            feedback += 'Got:\n\t"{0}"\n'.format(message)

            # print error and prevent from iterating.
            print feedback

    if VERBOSE:
        print '----'
        print

    if len(script):
        cmd, expected_output = script.pop(0)
        ws.expected_output = expected_output
        if VERBOSE:
            print 'Sending:'
            print cmd
            print
        ws.send(cmd)
    else:
        if VERBOSE:
            print
            print 'Closing.'
        ws.close()

if __name__ == "__main__":
    """
    if '-v' in sys.argv:
        VERBOSE = True
        websocket.enableTrace(True)

    ws = websocket.WebSocketApp('ws://{host}/cmd'.format(host=host_string),
                                on_message=on_message)
    ws.expected_output = None
    ws.run_forever()
    """
    #x = TestModel.create('key', data={ 'foo': 'bar' })
    #print x.foo
    unittest.main()


