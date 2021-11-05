#!/usr/bin/env python3
import ipaddress
import json
import requests
import ssl
from cloudvision.Connector.codec import Wildcard
from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector.codec.custom_types import FrozenDict
from cloudvision.Connector.codec import Wildcard, Path
from utils import pretty_print
import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

debug = False
switchesTemp = {}
def login(url_prefix, username, password):
    connect_timeout = 10
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    session = requests.Session()
    authdata = {"userId": username, "password": password}
    response = session.post(
        "https://" + url_prefix + "/cvpservice/login/authenticate.do",
        data=json.dumps(authdata),
        headers=headers,
        timeout=connect_timeout,
        verify=False,
    )
    if response.json()["sessionId"]:
        token = response.json()["sessionId"]
        sslcert = ssl.get_server_certificate((url_prefix, 443))
        return [token, sslcert]


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


def query_devices(client):
    pathElts = [
        "DatasetInfo",
        "Devices",
    ]
    dataset = "analytics"
    return get(client, dataset, pathElts)


def entmib(client,dId):
    pathElts = ["Sysdb",
                "hardware",
                "entmib",
                "chassis",
                "cardSlot",
                {"value":1}]
    pathElts2 = ["Sysdb",
                "hardware",
                "entmib",
                "chassis",
                "cardSlot",
                {"value":2}]
    switchesTemp[dId]['slot1'] = get(client, dId, pathElts)
    switchesTemp[dId]['slot2'] = get(client, dId, pathElts2)

def main(server, deviceId, token=None, certs=None, ca=None, key=None):
    cvp_user = "cvpadmin"
    cvp_pass = "arista"
    token = "token.txt"
    ca = "cert.crt"
    creds = login(server, cvp_user, cvp_pass)
    with open(token,"w") as f:
        f.write(creds[0])
    with open(ca, "w") as f:
        f.write(creds[1])
    client = get_client(f"{server}:443",token=token, key=key, ca=ca, certs=certs)
    devList = query_devices(client)
    # create list of streaming only devices
    activeDevList = [x for x in devList if 'status' in devList[x] and devList[x]['status'] == 'active']
    # remove vEOS-lab instances from the list
    phyList = [x for x in activeDevList if len(x)==11]
    futures_list = []
    # init dictionary with SN as key
    for x in phyList:
        switchesTemp[x] = {}
    # populate the switchesTemp using parallel execution
    with ThreadPoolExecutor(max_workers=20) as executor:
        for device in phyList:
            futures = executor.submit(entmib, client, device)
            futures_list.append(futures)

    # check if the switch has both SUP1 and SUP2
    dualSups = []
    for key, value in switchesTemp.items():
        if ('card' in value['slot1'] and value['slot1']['card'] is not None and
            'card' in value['slot2'] and value['slot2']['card'] is not None ):
            dualSups.append(key)
    print(dualSups)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server',required=True,help='Cloudvision server, e.g 10.10.10.10')
    args = parser.parse_args()
    server = args.server
    deviceId = args.deviceId
    main(server,deviceId)
