import copy
import json

REGISTRY = {}

class rjson(dict):
    def __init__(self, data):
        super(rjson, self).__init__(self, **data)

    def dict_get(self, *args, **kwargs):
        return super(rjson, self).__getitem__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):

        if 'key' in self.keys():
            key = super(rjson, self).__getitem__(*['key'])
            registry_data = REGISTRY.get(key)

            val = registry_data.dict_get(*args, **kwargs)
            #val = registry_data.__getitem__(*args, **kwargs)
        else:
            val = super(rjson, self).__getitem__(*args, **kwargs)

        #val = super(rjson, self).__getitem__(*args, **kwargs)

        return val

def register(payload):

    if not isinstance(payload, dict) and 'key' not in payload.keys():
        raise TypeError('Payload is not valid RJSON')

    if len(payload.keys()) > 1:
        REGISTRY[payload['key']] = rjson(payload)

def parse_json(payload):
    """
    Takes a JSON input and returns chunks of JSON
    with any related object is broken out into its
    own chunk.

    All chunks are returned.

    >>> parse_json('foo')
    'foo'

    >>> author = { 
    ...     'key': 'author',
    ...     'name': 'John'
    ... }
    >>> parse_json(author)
    {'key': 'author'}

    >>> book = {
    ...     'key': 'book',
    ...     'author': {
    ...         'key': 'authorJ',
    ...         'name': 'John',
    ...         'publisher': {
    ...             'key': 'publisherP',
    ...             'name': 'Publisher P'
    ...         }
    ...     }
    ... }
    >>> parse_json(book)
    [{'key': 'book'}, {'key': 'authorJ'}]
    """

    payload = copy.deepcopy(payload) 

    if not isinstance(payload, dict):
        return payload

    for k, v in payload.items():
        parsed = parse_json(v) # recurse
        payload[k] = parsed

    if 'key' in payload.keys():
        register(payload)
        return rjson({
            'key': payload['key']
        })

    return payload
if __name__ == "__main__":
    book = {
        'key': 'book',
        'author': {
            'key': 'authorJ',
            'name': 'John',
            'publisher': {
                'key': 'publisherP',
                'name': 'Publisher P'
            }
        },
        'name': 'A book',
    }
    parse_json(book)

    print REGISTRY['book']
    print type(REGISTRY['book'])
    print

    print REGISTRY['authorJ']
    print type(REGISTRY['authorJ'])
    print

    print REGISTRY['book']['author']
    print type(REGISTRY['book']['author'])
    print

    print REGISTRY['authorJ'] == REGISTRY['book']['author']


