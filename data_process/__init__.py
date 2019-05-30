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
                res = updateDict(res, dname, path, key, nominalKeys, value, time)
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
    for _, dset in resDict.items():
        for _, path in dset.items():
            for _, k in path.items():
                # grpc.Timestamp cannot be compared, hence the hack.
                timestamps = [(ts.seconds, ts.nanos) for ts in k["timestamps"]]
                _, _, k["values"], k["timestamps"] = zip(*sorted(zip(
                    timestamps,
                    # In case we have the same timestamp, keep ordering
                    range(len(timestamps)),
                    k["values"],
                    k["timestamps"])))
    return resDict
