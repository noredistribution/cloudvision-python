import sys
from AerisRequester.grpc_client import GRPCClient, CreateQuery
from AerisRequester.codec import Path, Wildcard
from utils import PrettyPrint


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
        CreateQuery([(pathElts, ["active"])], dId)
    ]

    with GRPCClient(apiserverAddr) as client:
        for batch in client.Get(query):
            for notif in batch["notifications"]:
                PrettyPrint(notif["updates"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: ", sys.argv[0], "<apiserverAddress> <datasetID>")
        exit(2)
    exit(main(sys.argv[1], sys.argv[2]))
