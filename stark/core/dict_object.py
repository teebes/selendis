
class DictObject(object):
    """
    >>> data = { 
    ...     "key": "foo", 
    ...     "relation": { 
    ...         "key": "bar" 
    ...     },
    ...     "collection": [
    ...         {
    ...             "key": "item",
    ...         }
    ...     ]
    ... }
    >>> dictobject = DictObject(data)
    >>> dictobject.key
    'foo'

    >>> dictobject.relation # doctest:+ELLIPSIS
    <DictObject - ...>
    >>> dictobject.relation.key
    'bar'

    >>> dictobject.collection #doctest:+ELLIPSIS
    [<DictObject - ...>]
    >>> dictobject.collection[0].key
    'item'
    """
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
            continue

            # an object
            if isinstance(v, dict):
                setattr(self, k, DictObject(v))

            # a collection
            elif isinstance(v, (list, tuple)):
                setattr(self, k, [
                    DictObject(item)
                    for item in v
                ])
            else:
                setattr(self, k, v)

    def __repr__(self):
        return u"<{cls} - {inst_id}>".format(
            cls=self.__class__.__name__,
            inst_id=id(self),
        )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
