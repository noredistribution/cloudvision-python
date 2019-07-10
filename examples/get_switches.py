import sys
from AerisRequester.grpc_client import GRPCClient, create_query
from utils import pretty_print


def main(apiserverAddr):
    pathElts = [
        "DatasetInfo",
        "Devices"
    ]
    query = [
        create_query([(pathElts, [])], "analytics")
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                pretty_print(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<apiserverAddress>")
        exit(2)
    exit(main(sys.argv[1]))
