import copy
import datetime
import json
import logging
import uuid

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from models import Character

LOG_LEVEL = 'info'
#LOG_LEVEL = 'debug'

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
console = logging.StreamHandler()
console.setLevel(getattr(logging, LOG_LEVEL.upper()))
logger.addHandler(console)

clients = {}

def inverse_direction(d):
    if d == 'north': return 'south'
    if d == 'east': return 'west'
    if d == 'south': return 'north'
    if d == 'west': return 'east'
    if d == 'up': return 'down'
    if d == 'down': return 'up'

    raise ValueError("Invalid direction {0}".format(d))

def command(cmd):
    pass

class CommandHandler(WebSocketHandler):
    """
    Central processor for websocket commands.

    Commands can be within certain contexts which
    are specific to the created user connection.

    Typically, a context will 'lock' the command
    processing until it's receied the command it
    thinks it should. 

    For example, if the context is 'auth', the command
    processor should expect either a username or a password.

    If a context is specified, then any message received from this
    user will be processed by the class method whose name is that of
    the context. So in the case of an authentication context, the
    'authentication' method will be used to process any messages
    received until the context is back to 'default'.
    """

    character = char = None
    context = None

    @property
    def root_context(self):
        try:
            return self.context.split('.')[0]
        except IndexError:
            return None

    @property
    def sub_context(self):
        try:
            return self.context.split('.')[1]
        except IndexError:
            return None

    def set_subcontext(self, subcontext):
        # TODO: use property setter?
        self.context = '{root}.{sub}'.format(
            root=self.root_context,
            sub=subcontext,
        )

    def open(self):
        self.ask_charname()

    def on_close(self):
        Character.online.pop(self.char.key)

    def on_message(self, message):

        logger.debug('IN: {0}'.format(message))

        if self.root_context is not None:
            return getattr(self, self.root_context)(message)
        else:
            return self.to_client('No context.')

    def on_close(self): pass

    def to_client(self, message):
        "Wrapper for messages being sent to clients"

        logger.debug('OUT: {0}'.format(message))

        _message = {
            "context": self.context,
            "message": message,
        }
        if self.context == 'default':
            _message["stats"] = {
                "hp": 100,
                "vision": "*",
            }

        try:
            super(CommandHandler, self).write_message(_message)
        except AttributeError: # can't write message to this client
            Character.online.pop(self.char.key)
            

    # ---- Outgoing

    # -- Room rendering
    def look_room(self):
        self.to_client(self.char.room.render(pov_char=self.char.key))

    def move(self, direction):
        origin_room = copy.copy(self.char.room)

        out = self.char.move(direction)
        self.to_client(out)

        # broadcast that char has left
        origin_room.broadcast(
            "{char} has left {dir}".format(
                char=self.char.key,
                dir=direction,
            ),
            exclude=[self.char.key],
        )

        # broadcast that char has arrived
        self.char.room.broadcast(
            "{char} has arrived from the {dir}".format(
                char=self.char.key,
                dir=inverse_direction(direction),
            ),
            exclude=[self.char.key],
        )

        self.look_room()

    def get_item(self, name):
        pass

    # -- Auth outgoing
    def ask_charname(self):
        self.context = 'authentication.get_charname'
        self.to_client('Enter your character name:')

    def welcome(self):
        Character.online[self.char.key] = self
        self.context = "default"
        self.to_client(
            "Welcome, {0}.".format(self.char.key)
        )
        self.look_room()

    # ---- Contexts
    def default(self, message):
        tokens = message.split(' ')

        if message.lower() in ('n', 'north'):
            self.move('north')
        elif message.lower() in ('e', 'east'):
            self.move('east')
        elif message.lower() in ('s', 'south'):
            self.move('south')
        elif message.lower() in ('w', 'west'):
            self.move('west')
        elif message.lower() in ('u', 'up'):
            self.move('up')
        elif message.lower() in ('d', 'down'):
            self.move('down')

        elif message.lower() == 'ping':
            self.to_client('pong!')

        if tokens[0] == 'get':
            self.get_item(tokens[1]) 

        else:
            self.look_room()

    def authentication(self, message):
        """
        Authentication flow:

        * `authentication.get_charname`:
            o if username exists:
                `default` (TODO: get passwd)
            o else :
                `authentication.query_char_creation`
        * `authentication.query_creation`
            o if 'yes':
                `default` (TODO: create passwd)
            o if 'no':
                `authentication.get_username`
        """

        if self.sub_context == 'get_charname':
            self._character_name = message
            character = Character.get(self._character_name)

            if character is None: # possible new character
                self.set_subcontext("query_char_creation")
                return self.to_client(
                    "Create character '{0}'? (Y/N)".format(self._character_name)
                )
    
            else: # existing character
                self.char = character
                return self.welcome()

        elif self.sub_context == 'query_char_creation':
            answer = message.lower()
            # new character
            if answer == 'y':
                self.char = Character.create(
                    self._character_name,
                    {
                        'level': 1,
                        'exp': 1,
                        'room_id': 1,
                        'inventory': []
                    }
                )

                self.context = 'default'
                return self.welcome()
                
            # go back to get_charname
            elif answer == 'n':
                return self.ask_charname()

        else:
            return self.to_client(
                'Unknown subcontext {0}'.format(self.sub_context)
            )
                

application = Application(
    [(r"/cmd", CommandHandler),],
    debug=True
)

if __name__ == "__main__":
    application.listen(8888)
    loop = IOLoop.instance()
    def tic(): 
        broadcast('tic')
        #for k, v in clients.items():
            #v.to_client('tic for %s' % k)
        loop.add_timeout(datetime.timedelta(seconds=20), tic)

    #loop.add_timeout(datetime.timedelta(seconds=1), tic)
    loop.start()

