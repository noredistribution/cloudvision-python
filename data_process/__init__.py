import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def ProcessNotifs(stream, paths=None, keys=None):
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
            if key is not None and key not in keys:
               continue
            res = updateDict(res, dname, path, key, None, time)
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
