import os
import sys

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curpath, '..')))

import json
import zmq
import appconfig as CONF


# class: FooManager
class FooManager(object):

    def __init__(self):
        serverAddr = "tcp://%s:%s" % ( CONF.entity_services['host'] , CONF.entity_services['port'])

        clientID = "WebServer-Client"

        context = zmq.Context()
        self.serviceSock = context.socket(zmq.REQ)
        self.serviceSock.connect(serverAddr)  

    def __makeRequest(self,request):
        print("Making request: %s" % request)
        self.serviceSock.send_json(request)
                
        msg = json.loads (self.serviceSock.recv())

        if(CONF.DEBUG_MODE):
            print("received: %s" % msg[2])
            print("data: %s" % msg[2])
        
        return msg

    def getInfo(self):
        '''Get a list of information'''
        request = [ "getEntityList",  dict()]
        response = self.__makeRequest(request)
        if response[0] == '200':
            return json.loads(response[2])
        else:
            return 'Error in retrieving list'
