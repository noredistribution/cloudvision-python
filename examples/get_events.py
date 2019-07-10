import sys
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from AerisRequester.grpc_client import GRPCClient, create_query
from utils import pretty_print


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
        create_query([(pathElts, [])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.get(query, start=start):
            for notif in batch["notifications"]:
                pretty_print(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<apiserverAddress>")
        exit(2)
    # Edit time range for events here
    exit(main(sys.argv[1]))
