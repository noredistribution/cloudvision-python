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
            for upd in notif["updates"]:
                print(json.dumps(upd, default=default, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: ", sys.argv[0], "<apiserverAddress> <deviceID> <intfID>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
