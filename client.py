import json
import sys
import threading

from websocket import create_connection
import websocket

host_string = '0.0.0.0:8888'

VERBOSE = False

def get_input():
    while True:
        cmd = raw_input()
        ws.send(cmd)
        if cmd == 'quit':
            print 'Goodbye!'
            ws.close()
            break
    

def on_message(ws, message):
    message = json.loads(message)
    print message['message']

if __name__ == "__main__":
    if '-v' in sys.argv:
        websocket.enableTrace(True)

    ws = websocket.WebSocketApp('ws://{host}/cmd'.format(host=host_string),
                                on_message=on_message)

    thread = threading.Thread(target=get_input)
    #thread.daemon = True
    thread.start()

    ws.expected_output = None
    ws.run_forever()

    
