import sys
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from AerisRequester.grpc_client import GRPCClient, create_query
from AerisRequester import process_notifs, sort_dict
import matplotlib.pyplot as plt
import matplotlib.dates as md

def main(apiserverAddr, dId, intfId, versions):
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
        create_query([(pathElts, ["outOctets"])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        stream = client.get(query, versions=versions)
        dataDict = process_notifs(stream)
        # Order by timestamps
        dataDict = sort_dict(dataDict)

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
    if len(sys.argv) < 4:
        print("usage: ", sys.argv[0], "<apiserverAddresss> <deviceID> <intfID> <versions>")
        exit(2)
    exit(main(*sys.argv[1:]))
