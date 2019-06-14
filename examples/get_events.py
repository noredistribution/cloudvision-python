import sys
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from AerisRequester.grpc_client import GRPCClient, CreateQuery
from AerisRequester.codec import frozendict, Path
from utils import PrettyPrint


def main(apiserverAddr, days=0, hours=1, minutes=0):
    startDtime = datetime.datetime.now() - datetime.timedelta(days=days,
                                                              hours=hours,
                                                              minutes=minutes)
    start = Timestamp().FromDatetime(startDtime)
    pathElts = [
        "events",
        "activeEvents"
    ]
    query = [
        CreateQuery([(pathElts, [])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.Get(query, start=start):
            for notif in batch["notifications"]:
                PrettyPrint(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<apiserverAddress>")
        exit(2)
    # Edit time range for events here
    exit(main(sys.argv[1]))
