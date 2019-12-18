import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from AerisRequester.grpc_client import GRPCClient, create_query
from utils import pretty_print
from parser import base


def main(apiserverAddr, token=None, cert=None, key=None, ca=None,
         days=0, hours=1, minutes=0):
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

    with GRPCClient(apiserverAddr, certs=cert, key=key,
                    token=token, ca=ca) as client:
        for batch in client.get(query, start=start):
            for notif in batch["notifications"]:
                pretty_print(notif["updates"])
    return 0


if __name__ == "__main__":
    args = base.parse_args()
    # Edit time range for events here
    exit(main(args.apiserver, cert=args.certFile,
              key=args.keyFile, token=args.tokenFile, ca=args.caFile))
