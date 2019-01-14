import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../gen/')))
from google.protobuf.timestamp_pb2 import Timestamp
import router_pb2 as rtr
import router_pb2_grpc as rtr_client
import notification_pb2 as ntf
import codec
import grpc

def CreateQuery(pathKeys, dId, dtype="device"):
   encoder = codec.Encoder()
   paths = []
   for path, key in pathKeys:
      if key is not None:
         key = [encoder.Encode(k) for k in key]
      paths.append(rtr.Path(
         keys=key,
         path_elements=[encoder.Encode(elt) for elt in path]
      ))
   return rtr.Query(
      dataset = ntf.Dataset(type=dtype, name=dId),
      paths = paths
   )

def CreateNotification(secs, nano, paths, deletes=None, updates=None, retracts=None):
   encoder = codec.Encoder()
   ts = Timestamp(seconds=secs, nanos=nano)
   if deletes is not None:
      dels = [encoder.Encode(d) for d in deletes]
   if updates is not None:
      upd = [ntf.Update(key=encoder.Encode(k), value=encoder.Encode(v)) for k, v in updates]
   if retracts is not None:
      ret = [encoder.Encoder(r) for r in retracts]
   pathElts = [encoder.Encode(elt) for elt in paths]
   return ntf.Notification(
      timestamp = ts,
      deletes = dels,
      updates = upd,
      retracts = ret,
      path_elements = pathElts
   )

class GRPCClient(object):

   def __init__(self, grpcAddr, certs=None):
      if certs is None:
         channel = grpc.insecure_channel(grpcAddr)
      else:
         with open(certs, "rb") as f:
            creds = grpc.ssl_channel_credentials(f.read())
         channel = grpc.secure_channel(grpcAddr, creds)
      self.__client = rtr_client.RouterV1Stub(channel)

      self.encoder = codec.Encoder()
      self.decoder = codec.Decoder()

   def Get(self, querries, start=None, end=None, versions=None):
      res = rtr.GetRequest(
         query=querries,
         start=start,
         end=end,
         versions=versions
      )
      stream = self.__client.Get(res)
      return stream

   def Subscribe(self, querries):
      req = rtr.SubscribeRequest(
         query=querries
      )
      stream = self.__client.Subscribe(req)
      return stream

   def Publish(self, dtype, dId, sync, compare, notifs):
      req = rtr.PublishRequest(
         batch = notf.NotificationBatch(
            dataset = ntf.Dataset(type=dtype, name=dId),
            notifications = notifs
         ),
         sync = sync,
         compare = compare
      )
      self.__client.Publish(req)

   def GetDatasets(self, types=[]):
      req = rtr.DatasetsRequest(
         types = types
      )
      stream = self.__client.GetDatasets(req)
      return stream

   def CreateDataset(self, dtype, dId):
      req = rtr.CreateDatasetRequest(
         ntf.Dataset(type=dtype, name=dId)
      )
      self.__client.CreateDataset(req)

   def DecodeNotificationBatch(self, batch):
      res = {
         "dataset": {
            "name": batch.dataset.name,
            "type": batch.dataset.type
         },
         "notifications": [self.DecodeNotification(n) for n in batch.notifications]
      }
      return res

   def DecodeNotification(self, notif):
      res = {
         "timestamp": {"seconds": notif.timestamp.seconds, "nanos": notif.timestamp.nanos},
         "deletes": [self.decoder.Decode(d) for d in notif.deletes],
         "updates": [(self.decoder.Decode(u.key), self.decoder.Decode(u.value)) for u in notif.updates],
         "retracts": [self.decoder.Decode(r) for r in notif.retracts],
         "path_elements": [self.decoder.Decode(elt) for elt in notif.path_elements]
      }
      return res
