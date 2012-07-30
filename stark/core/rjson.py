import json

class Singleton(object):
    """
    >>> s1=Singleton()
    >>> s2=Singleton()
    >>> id(s1) == id(s2)
    True
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Registry(Singleton):
    """
    >>> registry = Registry()
    >>> foo = object()

    >>> id(registry.set('foo', foo)) == id(foo)
    True

    >>> id(registry.get('foo') ) == id(foo)
    True

    >>> registry.set('foo', 'bar')
    'bar'
    >>> registry.get('foo')
    'bar'

    >>> registry.reset()
    >>> registry.get('foo') is None
    True
    """

    keys = {}

    def set(self, key, value):
        self.keys[key] = value
        return value

    def get(self, key):
        return self.keys.get(key)

    def reset(self, key={}):
        self.keys = key

    def has(self, key):
        return self.keys.has_key(key)


registry = Registry()
class RJSON(object):
    """
    Dictionary attributes become class attributes:
    >>> author = RJSON({'key': 'author', 'name':'john'})
    >>> author.key
    'author'
    >>> author.name
    'john'

    Copy of the original data is preserved
    >>> author._data['name']
    'john'

    References to other model instances can be used:
    >>> book = RJSON({ 'key':'book', 'author': { 'key':'author' } })
    >>> book.author.name
    'john'

    If a model defines an attribute, those elements need to be present:
    >>> class MyModel(RJSON):
    ...     foo = ""
    ...     def method(self): pass
    >>> MyModel({ "bar": "i", "key": "key" }) # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    KeyError: ... ('foo' is required by schema)

    But callables are not part of the schema:
    >>> not RJSON.get_schema().has_key('method')
    True
    """

    @classmethod
    def get_schema(cl):
        """
        >>> class Thing(RJSON):
        ...     foo = 'bar'
        >>> Thing.get_schema() == {'foo': 'bar'}
        True
        """
        schema = {
            k:v for k, v in cl.__dict__.items()
            if (k not in RJSON.__dict__.keys()
            and not hasattr(v, '__call__'))
        }
        return schema
 
    @classmethod
    def validate_schema(cl, data):
        for required_key, info in cl.get_schema().items():
            if required_key not in data.keys():
                raise KeyError("Key '{}' is required by the schema".format(
                    required_key
                ))


    def __new__(cls, data):

        if isinstance(data, (list, tuple)):
            collection = []
            for item in data:
                collection.append(RJSON(item))
            return collection

        if not isinstance(data, dict):
            return data

        # assert isinstance(data, dict)

        cls.validate_schema(data)

        # reference
        if data.has_key('key'):

            instance_in_registry = registry.get(data['key'])
            if instance_in_registry:

                if len(data.keys()) > 1:
                    instance_in_registry.update(data)

                return instance_in_registry
            else:
                new = super(RJSON, cls).__new__(cls)
                new.update(data)
                registry.set(data['key'], new)
                return new
        else:
            new = super(RJSON, cls).__new__(cls)
            new.update(data)
            return new

    def update(self, data):
        self._data = data
        for attr, payload in data.items():
            if isinstance(payload, dict):
                setattr(self, attr, RJSON(payload))
            elif isinstance(payload, (list, tuple)):
                setattr(self, attr, [])
                for listitem in payload:
                    if isinstance(listitem, dict):
                        listitem = RJSON(listitem)
                    getattr(self, attr).append(listitem)
            else:
                setattr(self, attr, payload)
        return self

    def __unicode__(self):
        return u"<{cls} - {key}: {dump}>".format(
            cls=self.__class__.__name__,
            key=getattr(self, 'key', ''),
            dump=self._data,
        )

    def __repr__(self): return self.__unicode__()

Model = RJSON

if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    author = RJSON({'key': 'author', 'name': {'first': 'john', 'last': 'doe'}})
    book = RJSON({'key':'book', 'author': { 'key':'author'}})

    print book.author


