import sys
from AerisRequester.grpc_client import GRPCClient, CreateQuery
from AerisRequester.codec.custom_types import Path
from utils import PrettyPrint


def main(apiserverAddr):
    pathElts = [
        "DatasetInfo",
        "Devices"
    ]
    query = [
        CreateQuery([(pathElts, [])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.Get(query):
            for notif in batch["notifications"]:
                PrettyPrint(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<apiserverAddress>")
        exit(2)
    exit(main(sys.argv[1]))
