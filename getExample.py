
import logging
import websocket
import json
import time
from templates import *
from wrpc import WRPC

keys = [
   "Ethernet1/1"
]

paths = [
   "/Smash/counters/ethIntf/StrataCounters/current/counter"
]

m = makeKeys(keys)
p = makePaths(paths, keys=m)

ws = WRPC('apiserver.staging.corp.arista.io')
ws.connect()
devices = ws.getDatasets()
querries = []
for val in devices:
   if val["name"] == 'analytics':
      continue
   querries.append(query(val["type"], val["name"], p))

r = getRequest(querries, end=int(time.time()*10**9), versions=5)
print(json.dumps(r, indent=2))

nominalKeys = [
   "statistics",
   "outOctets",
   "value"
]
res = ws.get(r, keys=nominalKeys)
print(json.dumps(res, indent=4))
