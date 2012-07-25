VERSION = (0, 1)

def get_version():
    """
    >>> get_version() # doctest:+ELLIPSIS
    '...'
    >>>
    """
    return '.'.join([ str(i) for i in VERSION])
