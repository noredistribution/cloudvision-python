import os, sys
import websocket
import json
import logging
import ssl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import templates
import data_process

class WRPC(object):
   def __init__(self, url):
      self.url = "ws://%s/api/v2/wrpc/"% (url)
      self.ws = None
      self.headers = []
      self.reqCount=0

   def connect(self):
      if self.headers:
         self.url = self.url.replace("ws://", "wss://")

      try:
         self.ws = websocket.create_connection(self.url, sslopt={
            "cert_reqs": ssl.CERT_NONE}, header=self.headers)
         print("got there")
      except Exception as e:
         logging.error(e)

   def authenticate(self, authUrl, userId, password):
      credentials = {
         "userId": userId,
         "password": password
      }
      headers = {
         "Accept": "application/json",
         "Content-Type": "application/json"
      }

      req = requests.post(
         authUrl, data=json.dumps(credentials),
         headers=headers, verify=False
      )
      if req.status_code == 200:
         self.headers = [
            'Cookie: session_id={}'.format(req.json()['sessionId']),
            'Cache-Control: no-cache',
            'Pragma: no-cache',
         ]
      else:
         logging.error("Could not autheticate, check your credentials")

   def getDatasets(self, types=[]):
      token = self.makeToken()
      r = templates.getDatasets(types=[], token=token)
      self.ws.send(json.dumps(r))
      res = []
      resp = json.loads(self.ws.recv())
      while "error" not in resp and self.checkToken(resp):
         res.extend(resp["result"]["datasets"])
         resp = json.loads(self.ws.recv())
      self.handleError(resp)
      self.updateToken()
      return res

   def get(self, req, keys=[]):
      token = self.makeToken()
      req["token"] = token
      self.ws.send(json.dumps(req))
      # Form of deviceId/path/pathKey/NomKey
      res = {}
      resp = json.loads(self.ws.recv())
      while "error" not in resp and self.checkToken(resp):
         res = data_process.updateRes(res, resp, keys)
         resp = json.loads(self.ws.recv())
      self.handleError(resp)
      self.updateToken()
      return res

   def publish(self, req):
      token = self.makeToken()
      req["token"] = token
      self.ws.send(json.dumps(req))
      resp = json.loads(self.ws.recv())
      self.handleError(resp)
      self.updateToken()

   def subscribe(self, req, keys=[]):
      token = self.makeToken()
      req["token"] = token
      logging.info("Running a subscribe request, stop using that connection for other requests")
      self.ws.send(json.dumps(req))
      resp = json.loads(self.ws.recv())
      if resp["status"]["message"] != "Active":
         logging.error("Something went wrong in the subscribe request")
         sys.exit(2)
      resp = json.loads(self.ws.recv())
      while "error" not in resp and self.checkToken(resp):
         # yield data_process.updateRes({}, resp, keys)
         yield resp
         resp = json.loads(self.ws.recv())
      self.handleError(resp)

   def handleError(self, resp):
      if "error" in resp and resp["error"] != "EOF":
         logging.error("Expected EOF, got %s\nReturning intermediate result" % str(resp))
   def makeToken(self):
      return "pythonRequest%s" % self.reqCount
   def checkToken(self, resp):
      respToken = resp.get("token", "")
      expected = self.makeToken()
      if respToken != expected:
         logging.error("Expected token to be %s but it is %s" % (expected, respToken))
         return False
      return True
   def updateToken(self):
      self.reqCount += 1
