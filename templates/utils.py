# Copyright (c) 2017 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
# Subject to Arista Networks, Inc.'s EULA.
# FOR INTERNAL USE ONLY. NOT FOR DISTRIBUTION.

def makeKeys(keys):
   res = {}
   for i in range(len(keys)):
      res["key"+str(i)] = {
         "key": keys[i]
      }
   return res

def makePaths(paths, t="EXACT", keys={}):
   res = []
   for p in paths:
      res.append(
         {
            "type": t,
            "path": p,
            "keys": keys
         }
      )
   # Remove empty keys
   res = [{k: v for k, v in entry.items() if v} for entry in res]
   return res

def makeUpdates(update):
   res = {}
   count = 0
   for k, v in update.items():
      res[k] = {
         "key": k,
         "value": v,
         "value_type": getValueType(v)
      }
      count += 1
   return res

def getValueType(val):
   if type(val) is dict:
      res = {}
      for k, v in val.items():
         res[k] = getValueType(v)
      return res
   elif type(val) is list:
      res = []
      for i in val:
         res.append(getValueType(i))
      return res
   else:
      return type(val).__name__
