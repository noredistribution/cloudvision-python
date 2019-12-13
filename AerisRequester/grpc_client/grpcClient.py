import AerisRequester.codec as codec
import AerisRequester.gen.notification_pb2 as ntf
import AerisRequester.gen.router_pb2 as rtr
import AerisRequester.gen.router_pb2_grpc as rtr_client

import grpc
import google.protobuf.timestamp_pb2 as pbts
from typing import List, Optional, Any, Tuple


def create_query(pathKeys: List[Any], dId: str, dtype: str = "device"):
    """
    create_query creates a protobuf query message with dataset ID dId
    and dataset type dtype.
    pathKeys must be of the form [([pathElts...], [keys...])...]
    """
    encoder = codec.Encoder()
    paths = [
        rtr.Path(
            keys=[encoder.encode(k) for k in keys],
            path_elements=[encoder.encode(elt) for elt in path],
        )
        for path, keys in pathKeys if keys is not None
    ]
    return rtr.Query(
        dataset=ntf.Dataset(type=dtype, name=dId),
        paths=paths
    )


def create_notification(ts: pbts.Timestamp,
                        paths: List[Any],
                        deletes: Optional[List[Any]] = None,
                        updates: Optional[List[Tuple[Any, Any]]] = None,
                        retracts: Optional[List[Any]] = None) \
        -> ntf.Notification:
    """
    create_notification creates a notification protobuf message.
    ts must be of the type google.protobuf.timestamp_pb2.Timestamp
    paths must be a list of path elements
    deletes and retracts, if present, must be lists of keys
    updates, if present, must be of the form [(key, value)...]
    """
    encoder = codec.Encoder()
    # An empty list would mean deleteAll so distinguish z/w empty and None
    dels = None
    if deletes is not None:
        dels = [encoder.encode(d) for d in deletes]

    upds = None
    if updates is not None:
        upds = [
            ntf.Notification.Update(
                key=encoder.encode(k),
                value=encoder.encode(v)) for k, v in updates
        ]
    rets = None
    if retracts is not None:
        rets = [encoder.encode(r) for r in retracts]

    pathElts = [encoder.encode(elt) for elt in paths]
    return ntf.Notification(
        timestamp=ts,
        deletes=dels,
        updates=upds,
        retracts=rets,
        path_elements=pathElts
    )


class GRPCClient(object):
    """
    GRPCClient implements the protobuf client as well as its methods.
    grpcAddr must be a valid apiserver adress in the format <ADDRESS>:<PORT>
    certs, if present, must be the path to the cert file.
    key, if present, must be the path to .pem key file.
    token, if present, must be the path a .tok user access token.

    """

    def __init__(self, grpcAddr: str, *, certs: str = None, key: str = None,
                 ca: str = None, token: str = None):

        if (certs is None or key is None) and token is None:
            self.channel = grpc.insecure_channel(grpcAddr)
        else:
            tokCreds = None
            if token:
                with open(token, 'rb') as f:
                    tokData = f.read()
                    tokCreds = grpc.access_token_call_credentials(tokData)

            certData = None
            if certs:
                with open(certs, 'rb') as f:
                    certData = f.read()
            keyData = None
            if key:
                with open(key, 'rb') as f:
                    keyData = f.read()
            caData = None
            if ca:
                with open(ca, 'rb') as f:
                    caData = f.read()

            creds = grpc.ssl_channel_credentials(certificate_chain=certData,
                                                 private_key=keyData,
                                                 root_certificates=caData)

            if tokCreds:
                creds = grpc.composite_channel_credentials(creds, tokCreds)

            self.channel = grpc.secure_channel(grpcAddr, creds)
        self.__client = rtr_client.RouterV1Stub(self.channel)

        self.encoder = codec.Encoder()
        self.decoder = codec.Decoder()

    # Make GRPCClient usable with `with` statement
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.channel.__exit__(type, value, traceback)

    def close(self):
        self.channel.close()

    def get(self, queries, start=None, end=None,
            versions=None, sharding=None):
        """
        Get creates and executes a Get protobuf message, returning a stream of
        notificationBatch.
        queries must be a list of querry protobuf messages.
        start and end, if present, must be nanoseconds timestamps (uint64).
        sharding, if present must be a protobuf sharding message.
         """
        request = rtr.GetRequest(
            query=queries,
            start=start,
            end=end,
            versions=versions,
            sharded_sub=sharding
        )
        stream = self.__client.Get(request)
        return (self.decode_batch(nb) for nb in stream)

    def subscribe(self, queries, sharding=None):
        """
        Subscribe creates and executes a Subscribe protobuf message,
        returning a stream of notificationBatch.
        queries must be a list of querry protobuf messages.
        sharding, if present must be a protobuf sharding message.
        """

        req = rtr.SubscribeRequest(
            query=queries,
            sharded_sub=sharding
        )
        stream = self.__client.Subscribe(req)
        return (self.decode_batch(nb) for nb in stream)

    def publish(self, dtype, dId, sync, compare, notifs):
        """
        Publish creates and executes a Publish protobuf message.
        refer to AerisRequester/protobufs/router.proto:124
        """
        req = rtr.PublishRequest(
            batch=ntf.NotificationBatch(
                d="device",
                dataset=ntf.Dataset(type=dtype, name=dId),
                notifications=notifs
            ),
            sync=sync,
            compare=compare
        )
        self.__client.Publish(req)

    def get_datasets(self, types=[]):
        """
        GetDatasets retrieves all the dataset streaming on Aeris
        types, if present, filter the querried dataset by types
        """
        req = rtr.DatasetsRequest(
            types=types
        )
        stream = self.__client.GetDatasets(req)
        return stream

    def create_dataset(self, dtype, dId):
        req = rtr.CreateDatasetRequest(
            dataset=ntf.Dataset(type=dtype, name=dId)
        )
        self.__client.CreateDataset(req)

    def decode_batch(self, batch):
        res = {
            "dataset": {
                "name": batch.dataset.name,
                "type": batch.dataset.type
            },
            "notifications": [self.decode_notification(n)
                              for n in batch.notifications]
        }
        return res

    def decode_notification(self, notif):
        res = {
            "timestamp": notif.timestamp,
            "deletes": [self.decoder.decode(d) for d in notif.deletes],
            "updates": {
                self.decoder.decode(u.key): self.decoder.decode(u.value)
                for u in notif.updates
            },
            "retracts": [self.decoder.decode(r) for r in notif.retracts],
            "path_elements": [
                self.decoder.decode(elt) for elt in notif.path_elements
            ]
        }
        return res
