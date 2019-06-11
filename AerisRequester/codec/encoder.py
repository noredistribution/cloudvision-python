import msgpack
import io
from AerisRequester.codec.custom_types import Float32, PointerType, WildcardType
from AerisRequester.codec.custom_types import Wildcard, Path

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
        for val in a:
            res += self.Encode(val)
        return res

    def EncodeMap(self, m):
        res = b""
        res += self.__packer.pack_map_header(len(m))
        dictItems = []
        for k, v in m.items():
            buf = b""
            buf += self.Encode(k)
            buf += self.Encode(v)
            dictItems.append(buf)
        res += b"".join(sorted(dictItems))
        return res

    def Encode(self, val):
        res = b""
        if isinstance(val, str):
            res += self.EncodeString(val)
        elif isinstance(val, Float32):
            res += msgpack.packb(val, use_single_float=True)
        elif isinstance(val, list):
            res += self.EncodeArray(val)
        elif isinstance(val, dict):
            res += self.EncodeMap(val)
        elif isinstance(val, Wildcard):
            print("Got there", val)
            res += self.__packer.pack(msgpack.ExtType(
                WildcardType, b""))
        elif isinstance(val, Path):
            keys = self.Encode(val._keys)
            res += self.__packer.pack(msgpack.ExtType(
                PointerType, keys))
        else:
            print("Got there wrongly", val, isinstance(val, Wildcard), Wildcard())
            res += self.__packer.pack(val)
        return res
