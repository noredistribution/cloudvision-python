PointerType = 0
WildcardType = 1


# Python doesn't differentiate between Float32 and 64
# This allows for the proper Marshalling of Float32
class Float32(float):
    pass


class Wildcard(object):
    pass


class hashdict(dict):
    def __key(self):
        return tuple(sorted(self.items()))

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return len(self) < len(other) or self.__key() < other.__key()

    def __eq__(self, other):
        return self.__key() == other.__key()


class Path(object):

    def __init__(self, keys=[]):
        self._keys = keys

    def __repr__(self):
        return self._keys.__str__()
