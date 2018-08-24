import logging
import json
import sys

def updateRes(res, resp, nomKeys):
   if "result" not in resp:
      logging.error("expected to have result in json but got %s" % json.dumps(resp, indent=2))
      sys.exit(2)
   data = resp["result"]
   dset = data["dataset"]["name"]

   for notif in data["notifications"]:
      ts = notif["timestamp"]
      path = notif["path"]
      if "updates" not in notif:
         continue
      for k, v in notif["updates"].items():
         targetVal = getVal(v["value"], nomKeys)
         res = updateDict(res, dset, path, k, nomKeys, targetVal, ts)
   return res

def getVal(nominal, nomKeys):
   res = nominal
   for k in nomKeys:
      if k not in res:
         logging.error(
"""
Key  %s not found in json %s
Full nominal %s
Nominal key path %s
""" % (k, res, nominal, nomKeys)
         )
         sys.exit(2)
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
