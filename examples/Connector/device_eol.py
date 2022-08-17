# Copyright (c) 2021 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

from copy import deepcopy
from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector.codec import Wildcard, Path, FrozenDict
from utils import pretty_print
from parser import base
from pprint import pprint as pp
import json

debug = False


def get(client, dataset, pathElts):
    ''' Returns a query on a path element'''
    result = {}
    query = [
        create_query([(pathElts, [])], dataset)
    ]

    for batch in client.get(query):
        for notif in batch["notifications"]:
            if debug:
                pretty_print(notif["updates"])
            result.update(notif["updates"])
    return result


def unfreeze(o):
    ''' Used to unfreeze Frozen dictionaries'''
    if isinstance(o, (dict, FrozenDict)):
        return dict({k: unfreeze(v) for k, v in o.items()})

    if isinstance(o, (str)):
        return o

    try:
        return [unfreeze(i) for i in o]
    except TypeError:
        pass

    return o

def getSwitchesInfo(client):
    pathElts = [
        "DatasetInfo",
        "Devices"
    ]
    dataset = "analytics"
    return get(client, dataset, pathElts)


def getDeviceLifecycles(client):
    pathElts = [
        "lifecycles",
        "devices",
        "hardware"
    ]
    dataset = "analytics"
    return get(client, dataset, pathElts)


def getDeviceLifecyclesSW(client):
    pathElts = [
        "lifecycles",
        "devices",
        "software"
    ]
    dataset = "analytics"
    return get(client, dataset, pathElts)


def main(apiserverAddr, token=None, certs=None, key=None, ca=None):

    with GRPCClient(apiserverAddr, token=token, key=key,
                    ca=ca, certs=certs) as client:
        hw_eol = getDeviceLifecycles(client)
        sw_eol = getDeviceLifecyclesSW(client)
        datasetInfo = getSwitchesInfo(client)
        eol_db = deepcopy(unfreeze(hw_eol))
        for k,v in unfreeze(sw_eol.items()):
            if k in eol_db:
                eol_db[k]['endOfSoftwareSupport'] = v
            else:
                eol_db[k] = {'endOfSoftwareSupport': v}
        if args.device:
            pp(eol_db[args.device])
        else:
            pp(eol_db)

    return 0


if __name__ == "__main__":
    base.add_argument("--device", type=str, help="device serial number")
    args = base.parse_args()
    exit(main(args.apiserver, certs=args.certFile, key=args.keyFile,
              ca=args.caFile, token=args.tokenFile))
