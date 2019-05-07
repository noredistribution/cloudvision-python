import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../')))
import grpc_client
import codec


def default(obj):
    if isinstance(obj, codec.Path):
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
        codec.Wildcard()
    ]
    query = [
        grpc_client.CreateQuery([(pathElts, ["active"])], dId)
    ]
    s = client.Get(query)
    for a in s:
        for notif in a["notifications"]:
            for upd in notif["updates"]:
                print(json.dumps(upd, default=default, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: ", sys.argv[0], "<apiserverAddress> <datasetID>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2]))
