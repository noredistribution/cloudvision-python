import sys
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector import process_notifs, sort_dict
import matplotlib.pyplot as plt
from parser import base


# this example is having some issues compared to others, I'm moving onto others
# for now
def main(apiserverAddr, dId, intfId, versions, token=None, cert=None,
         key=None, ca=None):
    versions = int(versions)
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
        create_query([(pathElts, [])], "analytics")
    ]

    with GRPCClient(apiserverAddr, token=token, certs=cert, key=key,
            ca=ca) as client:
        stream = client.get(query, versions=versions)
        dataDict = process_notifs(stream)
        # Order by timestamps
        dataDict = sort_dict(dataDict)
        print(dataDict)

        # Formatting dates
        vals = dataDict["analytics"]["/".join(pathElts)]["outOctets"]["values"]
        tss = dataDict["analytics"]["/".join(pathElts)]["outOctets"]["timestamps"]
        tsVals = [ts.seconds for ts in tss]
        # tsVals=[datetime.datetime.fromtimestamp(ts) for ts in tsVals]
        # ax=plt.gca()
        # xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        # ax.xaxis.set_major_formatter(xfmt)
        plt.plot(tsVals)
        plt.show()
    return 0


if __name__ == "__main__":
    base.add_argument("--versions", default=100, type=int,
                      help="number of versions (rates) to fetch")
    base.add_argument("--device", type=str, help="device to fetch rates for")
    base.add_argument("--interface", type=str, help="interface to fetch rates for")
    args = base.parse_args()

    exit(main(args.apiserver, args.device, args.interface, args.versions,
              cert=args.certFile, key=args.keyFile, token=args.tokenFile,
              ca=args.caFile))
