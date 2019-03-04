import msgpack
import codec.custom_types

def pair_hook(data):
   res = {}
   for k, v in data:
      if isinstance(k, dict):
         k = codec.custom_types.hashdict(k)
      res[k] = v
   return res

def ext_hook(code, data):
   decoder = Decoder()
   if code == codec.custom_types.PointerType:
      keys = decoder.Decode(data)
      return codec.custom_types.Path(keys=keys)
   elif code == codec.custom_types.WildcardType:
      return codec.custom_types.Wildcard()
   return msgpack.ExtType(code, data)

class Decoder(object):

   def __init__(self):
      self.__unpacker = msgpack.Unpacker(raw=False, object_pairs_hook=pair_hook,
                                         ext_hook=ext_hook)

   def DecodeArray(self, l):
      res = []
      for val in l:
         res.append(self.postProcess(val))
      return res


   def DecodeMap(self, m):
      res = codec.custom_types.hashdict()
      for k, v in m.items():
         res[self.postProcess(k)] = self.postProcess(v)
      return res

   def postProcess(self, b):
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
      return self.postProcess(res)
