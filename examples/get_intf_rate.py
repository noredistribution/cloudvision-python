import sys
from AerisRequester.grpc_client import GRPCClient, CreateQuery
from AerisRequester.codec import Path
from utils import PrettyPrint


def main(apiserverAddr, dId, intfId):
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
        CreateQuery([(pathElts, ["outOctets"])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.Subscribe(query):
            for notif in batch["notifications"]:
                PrettyPrint(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: ", sys.argv[0], "<apiserverAddress> <deviceID> <intfID>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
