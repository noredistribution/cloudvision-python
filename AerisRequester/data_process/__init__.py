import logging
from collections import deque

def ProcessNotifs(stream, paths=None, keys=None, nominalKeys=None):
    """
    ProcessNotifs consume the batch coming from stream and return them
    as a hierarchy of dataset, path, and keys. Allowing for faster access
    of a given time serie.
    """
    res = {}
    for batch in stream:
        dname = batch["dataset"]["name"]
        for notif in batch["notifications"]:
            time = notif["timestamp"]
            path = "/".join(notif["path_elements"])
            if paths is not None and path not in paths:
                continue
            for key, value in notif["updates"]:
                if keys is not None and key not in keys:
                    continue
                value = getVal(value, nominalKeys)
                res = updateDict(res, dname, path, key, nominalKeys, value, time)
    return res

def getVal(nominal, nomKeys):
    res = nominal
    if nomKeys is None:
        return res
    for k in nomKeys:
        if k not in res:
         logging.error(
"""
Key  %s not found in json %s
Full nominal %s
Nominal key path %s
""" % (k, res, nominal, nomKeys)
         )
         return None
        res = res[k]
    return res

def updateDict(resDict, dataset, path, key, nominalKeys, val, ts):
    entry = resDict.setdefault(dataset,
                               {}).setdefault(path,
                                              {}).setdefault(key, {})
    if nominalKeys:
        entry = entry.setdefault("/".join(nominalKeys), {})
    entry.setdefault("values", []).append(val)
    entry.setdefault("timestamps", []).append(ts)
    return resDict

def SortDict(resDict):
    """
    SortDict orders every timeseries in a hierarchy of dataset by its timestamps.
    """

    def sortTimeSerie(timeSerie):
        # grpc.Timestamp cannot be compared, hence the hack.
        timestamps = [(ts.seconds, ts.nanos) for ts in timeSerie["timestamps"]]
        _, _, timeSerie["values"], k["timestamps"] = zip(*sorted(zip(
            timestamps,
            # In case we have the same timestamp, keep ordering
            range(len(timestamps)),
            timeSerie["values"],
            timeSerie["timestamps"])))

    stack = [resDict]
    while stack:
        timeSerie = stack.pop()
        if "values" in timeSerie and "timestamps" in timeSerie:
            sortTimeSerie(timeSerie)
        else:
            map(lambda x: stack.append(x), timeSerie.values())
    return resDict
