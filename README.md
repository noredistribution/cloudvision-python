# AerisRequester

AerisRequester is a Python implementation of a GRPC client for Aeris. It takes care
of getting and publishing data and datasets, and also provides utilities for data
representation similar to the ones found in Aeris Query Language.

## Getting started

This is a small example advertising a few of the GRPC client capabilities.
This example prints info from all devices streaming into Aeris.

```
targetDataset = "analytics"
path = ["DatasetInfo", "Devices"]
# No filtering done on keys, accept all
keys = []
ProtoBufQuery = CreateQuery([(path, keys)], targetDataset)
with GRPCClient("http://MyApiserver:9093") as client:
     for notifBatch in client.Get([query]):
         for notif in notifBatch["notifications"]:
             # Get timestamp for all update here with notif.Timestamp
             PrettyPrint(notif["updates"])
```