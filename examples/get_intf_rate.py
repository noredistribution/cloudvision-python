import sys
from AerisRequester.grpc_client import GRPCClient, create_query
from utils import pretty_print


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
        create_query([(pathElts, ["outOctets"])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.subscribe(query):
            for notif in batch["notifications"]:
                pretty_print(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: ", sys.argv[0], "<apiserverAddress> <deviceID> <intfID>")
        exit(2)
    exit(main(*sys.argv[1:]))
