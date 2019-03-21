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
    exit(main(sys.argv[1]))
