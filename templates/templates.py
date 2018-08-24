import sys
import logging

headers = {
   # Token that will be used to check your response
   "token": "",
   # get|subscribe|publish
   "command": "",
   "params": {}
}

def getRequest(querries, start=None, end=None, versions=0, token=""):
   if not querries:
      logging.error("Querries must be non-empty")
      sys.exit(2)
   params = {
      "query": querries
   }
   if start:
      params["start"] = start
   if end:
      params["end"] = end
   if versions:
      params["versions"] = versions
   return {
      "token": token,
      "command": "get",
      "params": params
   }

def query(deviceType, deviceName, paths):
   if not (deviceType and deviceName and paths):
      logging.error("deviceType, deviceName, and path must be present and non empty")
      sys.exit(2)
   res = {
      "dataset": {
         # device or analytics
         "type": deviceType,
         "name": deviceName,
      },
      "paths": paths
   }
   return res

def getDatasets(token="", types=[]):
   return {
      "token": token,
      "command": "getDatasets",
      "params": {
         "types": types
      }
   }

def publishRequest(batch, sync, token=""):
   if not (batch and sync):
      logging.error("sync and batch must be non null")
      sys.exit(2)
   return {
      "token": "token",
      "command": "publish",
      "params": {
         "sync": sync,
         "batch": batch
      }
   }

def batch(deviceType, deviceName, notifications):
   if not (deviceType and deviceName and notifications):
      logging.error("deviceType, deviceName, and notifications must be present and non empty")
      sys.exit(2)
   res = {
      "dataset": {
         "type": deviceType,
         "name": deviceName
      },
      "notifications": notifications
   }
   return res

def notification(time, path, deletes, updates):
   return {
      "timestamp": time,
      "path": path,
      "deletes": deletes,
      "updates": updates
   }

def subscribeRequest(queries, token=""):
   if not queries:
      logging.error("queries must be non null")
      sys.exit(2)
   res = {
      "token": token,
      "command": "subscribe",
      "params": {
         "query": queries
      }
   }
   return res
