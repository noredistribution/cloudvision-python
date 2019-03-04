import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import datetime
import grpc_client
from google.protobuf.timestamp_pb2 import Timestamp
import json
import codec.custom_types

def default(obj):
   if isinstance(obj, codec.custom_types.Path):
      return obj._keys

def main(apiserverAddr):
   client = grpc_client.GRPCClient(apiserverAddr)
   pathElts = [
      "DatasetInfo",
      "Devices"
   ]
   query = [
      grpc_client.CreateQuery([(pathElts, [])], "analytics")
   ]
   notifBatches = client.Get(query)

   for batch in notifBatches:
      for notif in batch["notifications"]:
         for update in notif["updates"]:
            print(json.dumps(update, indent=2))
   return 0


if __name__ == "__main__":
   if len(sys.argv) < 2:
      print("usage: ", sys.argv[0], "<apiserverAddress>")
      exit(2)
   # Edit time range for events here
   exit(main(sys.argv[1]))
