import sys
import os
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../')))
import grpc_client
import codec
import data_process
import matplotlib.pyplot as plt
import matplotlib.dates as md

def main(apiserverAddr, dId, intfId, versions):
    versions = int(versions)
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

    stream = client.Get(query, versions=versions)
    dataDict = data_process.ProcessNotifs(stream)
    # Order by timestamps
    dataDict = data_process.SortDict(dataDict)

    # Formatting dates
    vals = dataDict["analytics"]["/".join(pathElts)]["outOctets"]["values"]
    tss = dataDict["analytics"]["/".join(pathElts)]["outOctets"]["timestamps"]
    tsVals = [ts.seconds for ts in tss]
    tsVals=[datetime.datetime.fromtimestamp(ts) for ts in tsVals]
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(tsVals, vals)
    plt.show()
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: ", sys.argv[0], "<apiserverAddresss> <deviceID> <intfID> <versions>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
