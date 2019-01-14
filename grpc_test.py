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

# start = time.strptime("8 Jan 19", "%d %b %y")
# creds = None
# # with open("/tmp/turbine-private2.pem", "rb") as f:
# #    bb = f.read()
# #    print(bb)
# #    creds = grpc.ssl_channel_credentials(bb)
# channel = grpc.insecure_channel("apiserver-noauth-grpc-v2.dev.corp.arista.io:11099")
# stub = pbg.RouterV1Stub(channel)




# stream = io.BytesIO()
# intf = "Logs"
# packer = msgpack.Packer(use_bin_type=True)
# # stream.write(packer.pack_array_header(len(intf)))
# bb = packer.pack(bytearray(intf, "utf-8"))
# kk = pbr.GetRequest(
#    query = [
#       pbr.Query(
#          dataset = pbn.Dataset(name="JPE15430511", type="device"),
#          paths = [
#             pbr.Path(
#                type=0,
#                path="/Smash/counters/strataDebugCounter/Strata-FixedSystem/current/intfDebugCounter",
#                keys=[bb]
#             )
#          ],
#       )
#    ],
#    start=int(time.mktime(start) * 10**9)
# )
# i = 0
# a = stub.Get(kk)
# print(a)
# print(kk)
# for f in a:
#    i += 1
#    print("got: %d" % i)
#    print(f)
# print(i)

# getDset = stub.GetDatasets(pbr.DatasetsRequest())
# for res in getDset:
#    print(res)

def createPathElts(s):
   return s.split("/")


bla = createPathElts("Smash/counters/ethIntf/SandCounters/current/counter")
print(bla)
client = grpc_client.GRPCClient("apiserver-noauth-grpc-v2.dev.corp.arista.io:11099")
querry = [
   grpc_client.CreateQuery([(bla, None)], "JPE15430511")
]
s = client.Subscribe(querry)
print(s)
for a in s:
   print(json.dumps(client.DecodeNotificationBatch(a)))
   print("end request")
