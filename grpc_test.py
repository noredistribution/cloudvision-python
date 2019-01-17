import sys, os
# Required otherwise the generated files get failed dependencies
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'gen/')))
import router_pb2 as pbr
import notification_pb2 as pbn
import router_pb2_grpc as pbg
import grpc
import time
import msgpack
import io
import struct
import grpc_client
import json
from google.protobuf.timestamp_pb2 import Timestamp

def createPathElts(s):
   return s.split("/")

def printTime(ts):
   grpcTs = Timestamp(seconds=ts["seconds"], nanos=ts["nanos"])
   print(grpcTs.ToJsonString())

client = grpc_client.GRPCClient("apiserver-noauth-grpc-v2.dev.corp.arista.io:11099")

##### GET Test
# pathElts = createPathElts("Turbines/config/traffic-anomaly-detector/custom")
pathElts = createPathElts("Smash/counters/ethIntf/SandCounters/current")
querry = [
   grpc_client.CreateQuery([(pathElts, ["TestGrpcPublish"])], "JPE15430511")
]
print(querry)
s = client.Get(querry)
for a in s:
   print(a)
   print("End batch")


####### GETDATASETS Test
s = client.GetDatasets()
for a in s:
   print(a)

###### Publish Test
ts = Timestamp()
ts.GetCurrentTime()
dId = "JPE15430511"
dtype = "device"
sync = True
compare = None
pathElts = createPathElts("Smash/counters/ethIntf/SandCounters/current")
update = [("TestGrpcPublish", "test")]
notifs = [grpc_client.CreateNotification(ts.seconds, ts.nanos, pathElts, updates=update)]
s = client.Publish(dtype, dId, sync, compare, notifs)
print(s, dir(s))

###### Subscribe Test
pathElts = createPathElts("Smash/counters/ethIntf/SandCounters/current")
querry = [
   grpc_client.CreateQuery([(pathElts, ["TestGrpcPublish"])], "JPE15430511")
]
print(querry)
s = client.Subscribe(querry)
for a in s:
   print(a)
   print("End batch")
