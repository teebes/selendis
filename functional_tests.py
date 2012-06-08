import json
import logging
import sys
import traceback

import redis
import websocket

from stark.utils import is_subdict

default_conn = redis.Redis()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

"Scripts are of the form [[input, output], ...]"

script = [ # try to login with non existing char
    [
        {
            u"context": u"authentication.get_charname",
            u"message": u"Enter your character name:",
        },
        u"doesnotexist",
        "New login",
    ],
    [ # don't create char
        { 
            u"context": u"authentication.query_char_creation",
            u"message": u"Create character 'doesnotexist'? (Y/N)"
        },
        u"n",
        "Don't create",
    ],
    [ # try to login with new user
        { 
            u"context": u"authentication.get_charname",
            u"message": u"Enter your character name:", 
        },
        u"testuser",
        "New Login",
    ],
    [ # create char
        {
            u"context": u"authentication.query_char_creation",
            u"message": u"Create character 'testuser'? (Y/N)"
        },
        u"y",
        "Create",
    ],
    [
        {
            u"context": u"default",
            u"message": u"Welcome, testuser."
        },
        None,
        "Welcome"
    ],
    [
        None, # should be the first look
        u"n",
        "Move north"
    ],
    [
        {
            u"context": u"default",
            u"message": u"You leave north."
        },
        None,
        "Leave north msg",
    ], [ None ], # new room location
]

VERBOSE = False

def close(ws):
    ws.close()
    default_conn.delete('character-testuser')
    

def next_script_line(script):
    """
    >>> next_script_line([[1, 2, 3]])
    (1, 2, 3)
    >>> next_script_line([[1, 2]])
    (1, 2)
    >>> next_script_line([[1]])
    (1, None)
    >>> next_script_line([[]])
    (None, None)
    >>> next_script_line([])
    Traceback (most recent call last):
        ...
    IndexError: pop from empty list
    """

    line = script.pop(0)

    try:
        output, cmd, title = line
        return output, cmd, title
    except ValueError: pass

    try:
        output, cmd = line
        return output, cmd, None
    except ValueError: pass

    try:
        output = line[0]
        return output, None, None
    except IndexError: pass

    return None, None, None

def on_message(ws, message):
    try:
        return _on_message(ws, message)
    except:
        logging.error(traceback.format_exc())
        close(ws)

def _on_message(ws, message):
    message = json.loads(message)

    logger.debug('\nReceived: {0}'.format(json.dumps(message, indent=4)))

    try:
        output, cmd, title = next_script_line(script)
    except IndexError: 
        close(ws)
        return

    if output is None:
        pass
    elif is_subdict(output, message):
        status = 'OK'
        if title:
            status += ' - ' + title
        logger.info(status)

    else:
        feedback = u""

        if title:
            feedback += '{0}:\n'.format(title)

        feedback += u'Expected:\n{thing}\n'.format(
            thing=json.dumps(output, indent=4)
        )
        feedback += u'Got:\n{thing}\n'.format(
            thing=json.dumps(message, indent=4)
        )

        logger.error(feedback)

        close(ws)

    if cmd:
        logger.debug('Sending: {cmd}'.format(cmd=cmd))
        ws.send(cmd)

    if not len(script): close(ws)
 
if __name__ == "__main__":
    if '-v' in sys.argv:
        console.setLevel(logging.DEBUG)
        
    if '-t' in sys.argv:
        websocket.enableTrace(True)

    default_conn.delete('character-testuser')

    host_string = '0.0.0.0:8888'
    connection_string = 'ws://{host}/cmd'.format(host=host_string)

    ws = websocket.WebSocketApp(connection_string, on_message=on_message)

    ws.run_forever()

