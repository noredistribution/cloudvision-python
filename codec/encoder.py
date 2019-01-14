import msgpack
import io
import codec.custom_types
from collections import OrderedDict

class Encoder(object):

   def __init__(self):
      self.__packer = msgpack.Packer(use_bin_type=True, use_single_float=False)
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
      elif isinstance(val, custom_types.Float32):
         res += msgpack.packb(val, use_single_float=True)
      elif isinstance(val, list):
         res += self.EncodeArray(val)
      elif isinstance(val, dict):
         res += self.EncodeMap(val)
      else:
         res += self.__packer.pack(val)
      return res
