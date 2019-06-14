from collections import Mapping
PointerType = 0
WildcardType = 1


# Python doesn't differentiate between Float32 and 64
# This allows for the proper Marshalling of Float32
class Float32(float):
    pass


class Wildcard(object):
    pass


class frozendict(Mapping):
    """
    An immutable wrapper around dictionaries that implements the complete :py:class:`collections.Mapping`
    interface. It can be used as a drop-in replacement for dictionaries where immutability is desired.
    """

    dict_cls = dict

    def __init__(self, *args, **kwargs):
        self._dict = self.dict_cls(*args, **kwargs)
        self._hash = None

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in self._dict.items():
                h ^= hash((key, value))
            self._hash = h
        return self._hash

    # Used in with sort_keys when dumping json
    def __gt__(self, other):
        return tuple(sorted(self._dict.items())) < tuple(sorted(other._dict.items()))

    def __eq__(self, other):
        return tuple(sorted(self._dict.items())) == tuple(sorted(other._dict.items()))

class Path(object):

    def __init__(self, keys=[]):
        self._keys = keys

    def __repr__(self):
        return self._keys.__str__()
