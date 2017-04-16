import os
import sys
import unittest
import datetime
import random
import zmq
import json

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curpath, '..')))

requestKey = str(random.randint(1,1000))
serverHost = "127.0.0.1"
serverPort = "7000"
serverAddr = "tcp://%s:%s" % (serverHost, serverPort)

clientID = "TestClient001"

context = zmq.Context()
clientSock = context.socket(zmq.REQ)
clientSock.connect(serverAddr)  

##################################################################
class ApiServerTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ApiServerTests, self).__init__(*args, **kwargs)
      

    #############################################################
    def makeRequest(self,request):
        print("Making request: %s" % request)
        clientSock.send_json(request)
                
        msg = json.loads (clientSock.recv())
        print (" CLIENT#%s: Response from server: %s\n" % (clientID, msg))

    ##################################################################
    def test1_AddEntity_expectnoerror(self):
        # Put in a Create request
        msgCounter = 1
        print ("\n CLIENT#%s: Create Entity:%s" %(clientID, requestKey))
        request = [ "createEntity",  dict( key = requestKey, data = dict( client = clientID, requestID = msgCounter ))]
        self.makeRequest(request)

        # Put in a get request
        print ("\n CLIENT#%s: Get Entity:%s" %(clientID, requestKey))
        request = [ "getEntity",  dict( key = requestKey )]
        self.makeRequest(request)

    ##################################################################
    def test2_EditEntity_expectnoerror(self):
        # Put in a Edit request
        msgCounter = 2
        print ("\n CLIENT#%s: Edit Entity:%s" %(clientID, requestKey))
        request = [ "editEntity",  dict( key = requestKey , data = dict( client = clientID, requestID = msgCounter, edited = True ))]
        self.makeRequest(request)

        # Put in a Get request
        print ("\n CLIENT#%s: Get Entity:%s" %(clientID, requestKey))
        request = ["getEntity",  dict( key = requestKey )]
        self.makeRequest(request)

    ##################################################################
    def test3_DeleteEntity_expectnoerror(self):
        msgCounter = 3
        # Put in a delete request
        print ("\n CLIENT#%s: Delete Entity:%s" %(clientID, requestKey))
        request = ["deleteEntity",  dict( key = requestKey )]
        self.makeRequest(request)

        # Put in a get request
        print ("\n CLIENT#%s: Get Entity List" %(clientID))
        request = [ "getEntityList",  dict()]
        self.makeRequest(request)

##################################################################
if __name__ == '__main__':
    unittest.main()
