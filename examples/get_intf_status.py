import sys
import os
import json
import AerisRequester.grpc_client as grpc_client
from AerisRequester.codec.custom_types import Path, Wildcard


def default(obj):
    if isinstance(obj, Path):
        return obj._keys


def main(apiserverAddr, dId):
    client = grpc_client.GRPCClient(apiserverAddr)
    pathElts = [
        "Sysdb",
        "interface",
        "status",
        "eth",
        "phy",
        "slice",
        "1",
        "intfStatus",
        Wildcard()
    ]
    query = [
        grpc_client.CreateQuery([(pathElts, ["active"])], dId)
    ]
    s = client.Get(query)
    for a in s:
        for notif in a["notifications"]:
            print(json.dumps(notif["updates"], default=default, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: ", sys.argv[0], "<apiserverAddress> <datasetID>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2]))
