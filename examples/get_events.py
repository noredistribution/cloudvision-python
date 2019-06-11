import sys
import os
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import json
import AerisRequester.grpc_client as grpc_client
from AerisRequester.codec.custom_types import hashdict, Path


def default(obj):
    if isinstance(obj, Path):
        return obj._keys


def main(apiserverAddr, days=0, hours=1, minutes=0):
    client = grpc_client.GRPCClient(apiserverAddr)
    startDtime = datetime.datetime.now() - datetime.timedelta(days=days,
                                                              hours=hours,
                                                              minutes=minutes)
    start = Timestamp().FromDatetime(startDtime)
    pathElts = [
        "events",
        "activeEvents"
    ]
    query = [
        grpc_client.CreateQuery([(pathElts, [])], "analytics")
    ]
    s = client.Get(query, start=start)
    for a in s:
        for notif in a["notifications"]:
            print(json.dumps(notif["updates"], default=default, indent=4, sort_keys=True, separators=(',', ': ')))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<apiserverAddress>")
        exit(2)
    # Edit time range for events here
    exit(main(sys.argv[1]))
