import sys
import os
from google.protobuf.timestamp_pb2 import Timestamp
import AerisRequester.grpc_client as grpc_client


def main(apiserverAddr, dId, path, key):
    client = grpc_client.GRPCClient(apiserverAddr)
    ts = Timestamp()
    ts.GetCurrentTime()

    # Boilerplate values for dtype, sync, and compare
    dtype = "device"
    sync = True
    compare = None

    pathElts = path.split("/")
    notifs = [grpc_client.CreateNotification(ts, pathElts, deletes=[key])]
    s = client.Publish(dtype, dId, sync, compare, notifs)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("usage: ", sys.argv[0], "<apiserverAddress>" +
              " <deviceID> <path> <key>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
