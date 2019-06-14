import msgpack
from .custom_types import Wildcard, WildcardType, frozendict, PointerType, Path
__all__ = ["Decoder"]


def pair_hook(data):
    res = frozendict({
        frozendict(k) if isinstance(k, dict) else k: v
        for k, v in data
    })
    return res


def ext_hook(code, data):
    decoder = Decoder()
    if code == PointerType:
        return Path(keys=decoder.Decode(data))
    elif code == WildcardType:
        return Wildcard()
    return msgpack.ExtType(code, data)


class Decoder(object):

    def __init__(self):
        self.__unpacker = msgpack.Unpacker(raw=False,
                                           object_pairs_hook=pair_hook,
                                           ext_hook=ext_hook)

    def DecodeArray(self, l):
        return [self.__postProcess(v) for v in l]

    def DecodeMap(self, m):
        return frozendict({
            self.__postProcess(k): self.__postProcess(v)
            for k, v in m.items()
        })

    def __postProcess(self, b):
        if isinstance(b, bytes):
            return b.decode("ascii")
        elif isinstance(b, list):
            return self.DecodeArray(b)
        elif isinstance(b, (dict, frozendict)):
            return self.DecodeMap(b)
        else:
            return b

    def Decode(self, buf):
        self.__unpacker.feed(buf)
        res = self.__unpacker.unpack()
        return self.__postProcess(res)
