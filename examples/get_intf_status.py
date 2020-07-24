# Copyright (c) 2020 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector.codec import Wildcard
from utils import pretty_print
from parser import base


def main(apiserverAddr, dId, token=None, cert=None, ca=None):
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
    base.add_argument("--deviceId",
                      help="device id/serial number to query intfStatus for")
    args = base.parse_args()

    exit(main(args.apiserverAddr, args.deviceId, token=args.tokenFile,
         cert=args.certFile, ca=args.caFile))
