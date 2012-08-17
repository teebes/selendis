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

    >>> registry.reset({'foo': 'bar'})
    >>> registry.get('foo') is None
    False
    >>> registry.get('foo')
    'bar'
    """

    keys = {}

    def set(self, key, value):
        self.keys[key] = value
        return value

    def get(self, key):
        return self.keys.get(key)

    def reset(self, *args, **kwargs):
        try:
            key = args[0]
        except IndexError:
            key = {}
        
        self.keys = key

    #def has(self, key):
    #    r = self.keys.has_key(key)
    #    return r


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
    """

    registry = Registry()

    @classmethod
    def get_schema(cls):
        """
        >>> class Thing(RJSON):
        ...     foo = 'bar'
        >>> Thing.get_schema() == {'foo': 'bar'}
        True
        """
        schema = {}
        for cl in cls.__bases__:
            schema = {
                k:v for k, v in cl.__dict__.items()
                if (k not in RJSON.__dict__.keys()
                and not hasattr(v, '__call__'))
            }
        return schema
 
    @classmethod
    def validate_schema(cl, data):
        """
        Verifies that a given payload is valid as per the class's
        attribute declarations.
 
        >>> class MyModel(RJSON):
        ...     foo = ""
        ...     def method(self): pass
        >>> MyModel.validate_schema({ "bar": "i", "key": "key" }) # doctest:+IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        KeyError: ... ('foo' is required by schema)

        """

        for required_key, info in cl.get_schema().items():
            # If the model being created is not a weak refererence
            # and is missing a required key
            fails_validation = bool(
                not (len(data.keys()) == 1 and data.has_key('key'))
                and required_key not in data.keys()
            )
            if fails_validation:
                raise KeyError("Key '{}' is required by the schema".format(
                    required_key
                ))


    def __new__(cls, data):

        # If we're being passed a collection of items,
        # process each model and return the collection of
        # objects
        if isinstance(data, (list, tuple)):
            collection = []
            for item in data:
                collection.append(cls(item))
            return collection

        if not isinstance(data, dict):
            return data

        # TODO: disabling validation for now due to ramifications of
        # passing sub structures that get validated as if they were
        # the top level of the structure
        #cls.validate_schema(data)

        # reference
        if data.has_key('key'):

            instance_in_registry = cls.registry.get(data['key'])
            if instance_in_registry:

                if len(data.keys()) > 1:
                    instance_in_registry.update(data)

                return instance_in_registry
            else:
                new = super(RJSON, cls).__new__(cls)
                new.update(data)
                cls.registry.set(data['key'], new)
                return new
        else:
            new = super(RJSON, cls).__new__(cls)
            new.update(data)
            return new

    def update(self, data):
        self._data = data
        for attr, payload in data.items():
            if isinstance(payload, dict):
                setattr(self, attr, self.__class__(payload))
            elif isinstance(payload, (list, tuple)):
                setattr(self, attr, [])
                for listitem in payload:
                    if isinstance(listitem, dict):
                        listitem = self.__class__(listitem)
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


