import logging
import websocket
import json
import time
from templates import *
from wrpc import WRPC
import yaml

delKeys = [
   # "test"
]
d = makeKeys(delKeys)

updates = yaml.load(open('newconfig.yml').read())
u = makeUpdates(updates)

path = "/Turbines/config/traffic-anomaly-detector/custom"

ts = int(time.time()*10**9)

notif = notification(ts, path, d, {})
b = batch("device", "analytics", [notif])
r = publishRequest(b, True)
print(json.dumps(r, indent=2))
ws = WRPC('ws://apiserver.staging.corp.arista.io/api/v2/wrpc/')
res = ws.publish(r)
