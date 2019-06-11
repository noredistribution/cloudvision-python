import sys
import os
import json
import AerisRequester.grpc_client as grpc_client
from AerisRequester.codec.custom_types import Path


def default(obj):
    if isinstance(obj, Path):
        return obj._keys


def main(apiserverAddr, dId, intfId):
    client = grpc_client.GRPCClient(apiserverAddr)
    pathElts = [
        "Devices",
        dId,
        "versioned-data",
        "interfaces",
        "data",
        intfId,
        "rates",
    ]
    query = [
        grpc_client.CreateQuery([(pathElts, ["outOctets"])], "analytics")
    ]
    s = client.Subscribe(query)
    for a in s:
        for notif in a["notifications"]:
                print(json.dumps(notif["updates"], default=default, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: ", sys.argv[0], "<apiserverAddress> <deviceID> <intfID>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
