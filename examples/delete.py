import sys
from google.protobuf.timestamp_pb2 import Timestamp
from AerisRequester.grpc_client import GRPCClient, create_notification


def main(apiserverAddr, dId, path, key):
    ts = Timestamp()
    ts.GetCurrentTime()

    # Boilerplate values for dtype, sync, and compare
    dtype = "device"
    sync = True
    compare = None

    pathElts = path.split("/")
    notifs = [create_notification(ts, pathElts, deletes=[key])]
    with GRPCClient(apiserverAddr) as client:
        s = client.publish(dtype, dId, sync, compare, notifs)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("usage: ", sys.argv[0], "<apiserverAddress>" +
              " <deviceID> <path> <key>")
        exit(2)
    exit(main(*sys.argv[1:]))
