from AerisRequester.grpc_client import GRPCClient, create_query

from utils import pretty_print
from parser import base


def main(apiserverAddr, token=None, certs=None, key=None):
    pathElts = [
        "DatasetInfo",
        "Devices"
    ]
    query = [
        create_query([(pathElts, [])], "analytics")
    ]

    with GRPCClient(apiserverAddr, token=token, key=key, certs=certs) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                pretty_print(notif["updates"])
    return 0


if __name__ == "__main__":
    args = base.parse_args()
    exit(main(args.apiserver, certs=args.certFile, key=args.keyFile,
              token=args.tokenFile))
