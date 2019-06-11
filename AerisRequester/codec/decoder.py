import msgpack
from .custom_types import Wildcard, WildcardType, hashdict, PointerType, Path
__all__ = ["Decoder"]


def pair_hook(data):
    res = {}
    for k, v in data:
        if isinstance(k, dict):
            k = hashdict(k)
        res[k] = v

    return res


def ext_hook(code, data):
    decoder = Decoder()
    if code == PointerType:
        keys = decoder.Decode(data)
        return Path(keys=keys)
    elif code == WildcardType:
        return Wildcard()
    return msgpack.ExtType(code, data)


class Decoder(object):

    def __init__(self):
        self.__unpacker = msgpack.Unpacker(raw=False,
                                           object_pairs_hook=pair_hook,
                                           ext_hook=ext_hook)

    def DecodeArray(self, l):
        res = []
        for val in l:
            res.append(self.__postProcess(val))
        return res

    def DecodeMap(self, m):
        res = hashdict()
        for k, v in m.items():
            res[self.__postProcess(k)] = self.__postProcess(v)
        return res

    def __postProcess(self, b):
        if isinstance(b, bytes):
            return b.decode("ascii")
        elif isinstance(b, list):
            return self.DecodeArray(b)
        elif isinstance(b, dict):
            return self.DecodeMap(b)
        else:
            return b

    def Decode(self, buf):
        self.__unpacker.feed(buf)
        res = self.__unpacker.unpack()
        return self.__postProcess(res)
