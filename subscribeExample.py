
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
   "/events/activeEvents"
]

m = makeKeys(keys)
p = makePaths(paths, keys={})
q = query("device", "analytics", p)

ws = WRPC('apiserver.staging.corp.arista.io')
ws.connect()
r = subscribeRequest([q])
print(json.dumps(r, indent=2))

res = ws.subscribe(r)
for r in res:
   print(json.dumps(r, indent=4))
