def is_subdict(subset, superset):
    """ 
    >>> is_subdict({ 'foo': 'bar' }, { 'foo': 'bar', 'extra': 'thing' })
    True
    >>> is_subdict({ 'foo': 'baz' }, { 'other': 'thing' })
    False
    >>> is_subdict({ 'a': 1, 'b': 2 }, { 'a': 1, 'b': 2, 'c': 3 })
    True
    >>> is_subdict({ 'a': 1, 'b': 2 }, { 'a': 1, 'b': 1 })
    False
    >>> subset = {u'message': u'Welcome, testuser.', u'context': u'default'}
    >>> superset = {u'message': u'Welcome, testuser.', u'stats': {u'hp': 100, u'vision': u'*'}, u'context': u'default'}
    >>> is_subdict(subset, superset)
    True
    """

    return all(item in superset.items() for item in subset.items())
