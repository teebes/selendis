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
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
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
    A data payload is required:
    >>> Model() # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: ... (need to pass in data)

    A key is required in data:
    >>> Model({}) # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    KeyError: ... ('key' is required in data)

    Dictionary attributes become class attributes:
    >>> author = Model({'key':'author', 'name':'john'})
    >>> author.key
    'author'
    >>> author.name
    'john'
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
    >>> model = MyModel({ "foo": "i", "key": "key" })
    >>> not model.get_schema().has_key('method')
    True
    >>> model
    <MyModel - key>
    """

    key = "required"

    @classmethod
    def validate_schema(cl, data):
        for required_key, info in cl.get_schema().items():
            if required_key not in data.keys():
                raise KeyError("Key '{}' is required by the schema".format(
                    required_key
                ))
    
    def __init__(self, data):
        self.__class__.validate_schema(data)

        self._data = data

        for k, v in data.items():

            # model relation
            if isinstance(v, dict):
                if registry.has(v['key']):
                    setattr(self, k, registry.get(v['key']))
                else:
                    setattr(self, k, Model(v))

            # collection
            elif isinstance(v, (list, tuple)):
                for item in v:
                    instance_in_registry = registry.get(v['key'])
                    if instance_in_registry is None:
                        setattr(self, k, Model(v))
                    else:
                        setattr(self, k, instance_in_registry)
                    
            else:
                setattr(self, k, v)

        registry.set(self.key, self)

    @classmethod
    def get_schema(cl):
        """
        >>> class Thing(Model):
        ...     foo = 'bar'
        >>> Thing.get_schema() == {'foo': 'bar', 'key': 'required'}
        True
        """
        schema = {
            k:v for k, v in cl.__dict__.items()
            if (k not in Model.__dict__.keys()
            and not hasattr(v, '__call__'))
        }
        schema['key'] = cl.key
        return schema

    def __unicode__(self):
        return u"<{cls} - {key}>".format(
            cls=self.__class__.__name__,
            key=self.key
        )

    def __repr__(self): return self.__unicode__()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

