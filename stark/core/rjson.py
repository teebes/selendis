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
class Model(object):
    """
    Dictionary attributes become class attributes:
    >>> author = Model({'key': 'author', 'name':'john'})
    >>> author.key
    'author'
    >>> author.name
    'john'

    Copy of the original data is preserved
    >>> author._data['name']
    'john'

    References to other model instances can be used:
    >>> book = Model({ 'key':'book', 'author': { 'key':'author' } })
    >>> book.author.name
    'john'

    If a model defines an attribute, those elements need to be present:
    >>> class MyModel(Model):
    ...     foo = ""
    ...     def method(self): pass
    >>> MyModel({ "bar": "i", "key": "key" }) # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    KeyError: ... ('foo' is required by schema)

    But callables are not part of the schema:
    >>> not Model.get_schema().has_key('method')
    True
    """

    @classmethod
    def get_schema(cl):
        """
        >>> class Thing(Model):
        ...     foo = 'bar'
        >>> Thing.get_schema() == {'foo': 'bar'}
        True
        """
        schema = {
            k:v for k, v in cl.__dict__.items()
            if (k not in Model.__dict__.keys()
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
        assert isinstance(data, dict)

        cls.validate_schema(data)

        # reference
        if data.has_key('key'):
            instance_in_registry = registry.get(data['key'])
            if instance_in_registry and len(data.keys()) == 1:
                return instance_in_registry

        new = super(Model, cls).__new__(cls)

        new.update(data)
        if len(data.keys()) > 1 and data.has_key('key'):
            registry.set(data['key'], new)

        return new

    def update(self, data):
        self._data = data
        for attr, payload in data.items():
            if isinstance(payload, dict):
                setattr(self, attr, Model(payload))
            elif isinstance(payload, (list, tuple)):
                pass
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()


