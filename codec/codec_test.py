import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import yaml
import codec.encoder
import codec.decoder
import logging
import codec.custom_types
import numpy as np
import msgpack

def makeComplex(l):
   res = codec.custom_types.hashdict()
   for  i in range(0, len(l), 2):
      k = l[i]
      if isinstance(k, dict):
         k = codec.custom_types.hashdict(k)
      res[k] = l[i+1]
   return res

def runTest(encoder, decoder, test, valType):
   expected = bytearray(test["out"])
   inp = test[valType]
   if valType == "i64":
      inp = int(test[valType])
   if valType == "f32":
      inp = codec.custom_types.Float32(np.float32(test[valType]))
   if valType == "f64":
      inp = float(test[valType])
   if valType == "bytes":
      inp = bytes(test[valType])
   if valType == "complex":
      inp = makeComplex(test[valType])
   if valType == "pointer":
      inp = msgpack.ExtType(0, encoder.Encode(test[valType]))
   res = encoder.Encode(inp)
   if res != expected:
      logging.error("Bad encoding for %s. Got %s expected %s" % (test["name"], res, expected))
      print(inp)
      print(decoder.Decode(expected))
      print(decoder.Decode(res))
      return

   rev = decoder.Decode(res)
   if rev != inp:
      logging.error("Bad decoding for %s. Got %s expected %s" % (test["name"], rev, inp))
      return

   print("Test passed for: ", test["name"])

with open("codec_test.yml", "r", encoding="ascii") as f:
   testDict = yaml.load(f.read())

encoder = codec.encoder.Encoder()
decoder = codec.decoder.Decoder()

testTypes = [
   "bools",
   "i8",
   "i16",
   "i32",
   "i64",
   "f32",
   "f64",
   "str",
   "bytes",
   "array",
   "map",
   "complex",
   "pointer"
]

for t in testDict["tests"]:
   for typ in testTypes:
      if typ in t:
         runTest(encoder, decoder, t, typ)
