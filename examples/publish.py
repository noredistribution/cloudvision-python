import sys
from google.protobuf.timestamp_pb2 import Timestamp
from AerisRequester.grpc_client import GRPCClient, CreateNotification


def main(apiserverAddr, dId, path, key, value):
    ts = Timestamp()
    ts.GetCurrentTime()

    # Boilerplate values for dtype, sync, and compare
    dtype = "device"
    sync = True
    compare = None

    pathElts = path.split("/")
    update = [(key, value)]
    notifs = [CreateNotification(ts, pathElts, updates=update)]
    with GRPCClient(apiserverAddr) as client:
        client.Publish(dtype, dId, sync, compare, notifs)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("usage: ", sys.argv[0], "<apiserverAddress> " +
              "<deviceID> <path> <key> <value>")
        exit(2)
    # Edit time range for events here
    exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
