import sys
import os
import json
import AerisRequester.grpc_client as grpc_client
from AerisRequester.codec.custom_types import Path


def default(obj):
    if isinstance(obj, Path):
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
            print(json.dumps(notif["updates"], indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<apiserverAddress>")
        exit(2)
    exit(main(sys.argv[1]))
