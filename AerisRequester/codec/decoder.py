import msgpack
from .custom_types import Wildcard, WildcardType, FrozenDict, PointerType, Path
__all__ = ["Decoder"]


def pair_hook(data):
    res = FrozenDict({
        FrozenDict(k) if isinstance(k, dict) else k: v
        for k, v in data
    })
    return res


def ext_hook(code, data):
    decoder = Decoder()
    if code == PointerType:
        return Path(keys=decoder.decode(data))
    elif code == WildcardType:
        return Wildcard()
    return msgpack.ExtType(code, data)


class Decoder(object):

    def __init__(self):
        self.__unpacker = msgpack.Unpacker(raw=False,
                                           object_pairs_hook=pair_hook,
                                           ext_hook=ext_hook)

    def decode_array(self, l):
        return [self.__postProcess(v) for v in l]

    def decode_map(self, m):
        return FrozenDict({
            self.__postProcess(k): self.__postProcess(v)
            for k, v in m.items()
        })

    def __postProcess(self, b):
        if isinstance(b, bytes):
            return b.decode("ascii")
        elif isinstance(b, list):
            return self.decode_array(b)
        elif isinstance(b, (dict, FrozenDict)):
            return self.decode_map(b)
        else:
            return b

    def decode(self, buf):
        self.__unpacker.feed(buf)
        res = self.__unpacker.unpack()
        return self.__postProcess(res)
