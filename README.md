# AerisRequester

AerisRequester is a Python implementation of a GRPC client for Aeris. It takes care
of Getting and publishing data and datasets, and also provides utilities for data
representation similar to the ones found in Aeris Query Language.

## Getting started

This is a small example advertising a few of the GRPC client capabilities.
This example print info from all devices streaming on Aeris.

```
targetDataset = "analytics"
path = ["DatasetInfo", "Devices"]
# No filtering done on keys, accept all
keys = []
client = grpc_client.GRPCClient("http://MyApiserver:9093")
ProtoBufQuery = grpc_client.CreateQuery([(path, keys)], targetDataset)
notifBatchStream = client.Get([query])

for notifBatch in notifBatchStream:
   for notif in notifBatch["notifications"]:
      # Get timestamp for all update here with notif.Timestamp
      for update in notif["updates"]:
         print(update)

```