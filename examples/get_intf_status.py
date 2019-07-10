import sys
from AerisRequester.grpc_client import GRPCClient, create_query
from AerisRequester.codec import Wildcard
from utils import pretty_print


def main(apiserverAddr, dId):
    pathElts = [
        "Sysdb",
        "interface",
        "status",
        "eth",
        "phy",
        "slice",
        "1",
        "intfStatus",
        Wildcard()
    ]
    query = [
        create_query([(pathElts, ["active"])], dId)
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                pretty_print(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: ", sys.argv[0], "<apiserverAddress> <datasetID>")
        exit(2)
    exit(main(*sys.argv[1:]))
