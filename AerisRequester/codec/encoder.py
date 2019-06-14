import msgpack
import io
from AerisRequester.codec import Float32, PointerType, WildcardType
from AerisRequester.codec import Wildcard, Path, frozendict

class Encoder(object):

    def __init__(self):
        self.__packer = msgpack.Packer(use_bin_type=True,
                                       use_single_float=False)
        self.__buffer = io.BytesIO()

    def EncodeString(self, s):
        return self.__packer.pack(bytearray(s, "ascii"))

    def EncodeArray(self, a):
        res = b""
        res += self.__packer.pack_array_header(len(a))
        res += b"".join(self.Encode(val) for val in a)
        return res

    def EncodeMap(self, m):
        res = b""
        res += self.__packer.pack_map_header(len(m))
        dictItems = []
        for k, v in m.items():
            buf = b"".join((self.Encode(k), self.Encode(v)))
            dictItems.append(buf)
        res += b"".join(sorted(dictItems))
        return res

    def Encode(self, val):
        res = b""
        if isinstance(val, str):
            res = self.EncodeString(val)
        elif isinstance(val, Float32):
            res = msgpack.packb(val, use_single_float=True)
        elif isinstance(val, list):
            res = self.EncodeArray(val)
        elif isinstance(val, (dict, frozendict)):
            res = self.EncodeMap(val)
        elif isinstance(val, Wildcard):
            res = self.__packer.pack(msgpack.ExtType(
                WildcardType, b""))
        elif isinstance(val, Path):
            keys = self.Encode(val._keys)
            res = self.__packer.pack(msgpack.ExtType(
                PointerType, keys))
        else:
            res = self.__packer.pack(val)
        return res
