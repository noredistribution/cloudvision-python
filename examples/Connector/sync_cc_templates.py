# Copyright (c) 2020 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

# Synchronizes CVP Event Generation Configuration between two clusters
#
# Usage:
# python3 sync_cc_templates.py --src=192.0.2.174:8443 --srcauth=token,token1.txt,cvp1.crt \
#  --dst=192.0.2.178:8443 --dstauth=token,token2.txt,cvp2.crt
#
# gRPC Port for rAPI/Connector
# - 8443 (2020.2.0 - 2021.2.2)
# - 443 (2021.3.0 or newer and CVaaS)

import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from cloudvision.Connector.grpc_client import GRPCClient, create_query, create_notification
from cloudvision.Connector.codec.custom_types import FrozenDict
from cloudvision.Connector.codec import Wildcard, Path
from utils import pretty_print
from dst_parser import add_arguments
import json
import argparse

debug = False


def get_client(apiserverAddr, token=None, certs=None, key=None, ca=None):
    ''' Returns the gRPC client used for authentication'''
    return GRPCClient(apiserverAddr, token=token, key=key, ca=ca, certs=certs)


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


def getCcPath(client):
    ''' Returns all turbine config pointers'''
    pathElts = [
        "changecontrol"
    ]
    dataset = "cvp"
    return unfreeze(get(client, dataset, pathElts))


def getCcPathVersions(client, cc_type):
    ''' Returns all turbine config pointers'''
    pathElts = [
        "changecontrol",
        cc_type
    ]
    dataset = "cvp"
    return unfreeze(get(client, dataset, pathElts))

def getCcTemplates(client):
    ''' Returns all turbine config pointers'''
    pathElts = [
        "changecontrol",
        "template",
        "v1",
        Wildcard()
    ]
    dataset = "cvp"
    return unfreeze(get(client, dataset, pathElts))


def getCcActionBundles(client):
    ''' Returns all turbine config pointers'''
    pathElts = [
        "changecontrol",
        "actionBundle",
        "v1",
        Wildcard()
    ]
    dataset = "cvp"
    return unfreeze(get(client, dataset, pathElts))


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

def publish(client, dataset, pathElts, data={}):
    ''' Publish function used to update specific paths in the database'''
    ts = Timestamp()
    ts.GetCurrentTime()

    # Boilerplate values for dtype, sync, and compare
    dtype = "device"
    sync = True
    compare = None

    updates = []
    for dataKey in data.keys():
        dataValue = data.get(dataKey)
        updates.append((dataKey, dataValue))

    notifs = [create_notification(ts, pathElts, updates=updates)]

    client.publish(dtype=dtype, dId=dataset, sync=sync, compare=compare, notifs=notifs)
    return 0


def backupConfig(serverType, data):
    ''' Saves data in a json file'''
    filename = "backup" + str(serverType) + ".json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    ds = ("Synchronizes CVP Templates and Action Bundles between two clusters\n"
          "Usage:\n"
          "\tpython3 sync_cc_templates.py --src=10.83.12.79:8443 --srcauth=token,token1.txt,cvp1.crt "
          "--dst=10.83.12.173:8443 --dstauth=token,token2.txt,cvp2.crt"
          )
    base = argparse.ArgumentParser(description=ds,
                                   formatter_class=argparse.RawTextHelpFormatter)
    add_arguments(base)
    args = base.parse_args()
    # Authenticate to the source and destination CVP servers
    clientSrc = get_client(args.src, certs=args.certFile, key=args.keyFile,
                           token=args.tokenFile, ca=args.caFile)
    clientDst = get_client(args.dst, certs=args.certFileDst, key=args.keyFileDst,
                           token=args.tokenFileDst, ca=args.caFileDst)
    # backup the event configurations from each server
    # this will create 4 files:
    #    - backupsource-cvp-tmpl.json
    #    - backupdest-cvp-tmpl.json
    #    - backupsource-cvp-ab.json
    #    - backupdest-cvp-ab.json

    source_templates = getCcTemplates(clientSrc)
    dest_templates = getCcTemplates(clientDst)
    source_action_bundles = getCcActionBundles(clientSrc)
    dest_action_bundles = getCcActionBundles(clientDst)

    backupConfig('source-cvp-tmpl', source_templates)
    backupConfig('dest-cvp-tmpl', dest_templates)
    backupConfig('source-cvp-ab', source_action_bundles)
    backupConfig('dest-cvp-ab', dest_action_bundles)

    # Check if the pointers already exist
    # If there were no templates/actionBundles created previously we have to populate these first
    dataset = 'cvp'
    pList = ['template', 'actionBundle']
    cc_ptrs = getCcPath(clientDst)

    ccv2 = getCcPathVersions(clientDst, "template")
    for ptr in pList:
        if ptr not in list(cc_ptrs.keys()):
            pathElts = ["changecontrol"]
            ptrData = {ptr: Path(keys=["changecontrol", ptr])}
            publish(clientDst, dataset, pathElts, ptrData)
        if ccv2 == {}:
            pathElts = ["changecontrol", ptr]
            ptrData = {"v1": Path(keys=["changecontrol", ptr, "v1"])}
            publish(clientDst, dataset, pathElts, ptrData)

    # Publish the CC templates to the target cluster
    for tmpl_key in source_templates:
        pathElts = ["changecontrol","template","v1", tmpl_key]
        update = {tmpl_key: source_templates[tmpl_key]}
        publish(clientDst, dataset, pathElts, update)
        ptrData = {tmpl_key: Path(keys=["changecontrol","template","v1", tmpl_key])}
        publish(clientDst, dataset, pathElts[:-1], ptrData)

    # Publish the CC Action Bundles to the target cluster
    for ab_key in source_action_bundles:
        pathElts = ["changecontrol","actionBundle","v1", ab_key]
        update = {ab_key: source_action_bundles[ab_key]}
        publish(clientDst, dataset, pathElts, update)
        ptrData = {ab_key: Path(keys=["changecontrol","actionBundle","v1", ab_key])}
        publish(clientDst, dataset, pathElts[:-1], ptrData)
