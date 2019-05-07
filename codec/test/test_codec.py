import os
import sys
import numpy as np
import yaml
import logging
import msgpack
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
import codec


# makeComplex creates a complex dictionary using a list of pairs
def makeComplex(l):
    res = codec.hashdict()
    for i in range(0, len(l), 2):
        k = l[i]
        if isinstance(k, dict):
            k = codec.hashdict(k)
        res[k] = l[i+1]
    return res


def runTest(encoder, decoder, test, valType):
    expected = bytearray(test["out"])
    inp = test[valType]
    if valType == "i64":
        inp = int(inp)
    if valType == "f32":
        inp = codec.custom_types.Float32(np.float32(inp))
    if valType == "f64":
        inp = float(inp)
    if valType == "bytes":
        inp = bytes(inp)
    if valType == "complex":
        inp = makeComplex(inp)
    if valType == "pointer":
        inp = msgpack.ExtType(0, encoder.Encode(inp))
    res = encoder.Encode(inp)
    if res != expected:
        logging.error("Bad encoding for %s. Got %s expected %s"
                      % (test["name"], res, expected))
        return
    rev = decoder.Decode(res)
    if rev != inp:
        logging.error("Bad decoding for %s. Got %s expected %s"
                      % (test["name"], rev, inp))
        return

    print("Test passed for: ", test["name"])


with open("test_codec.yml", "r", encoding="ascii") as f:
    testDict = yaml.load(f.read())

encoder = codec.Encoder()
decoder = codec.Decoder()

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
