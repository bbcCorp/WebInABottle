import multiprocessing
import zmq
import time
import random
import os
import sys
curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(  os.path.abspath( os.path.join(curpath,"..")) )
from mod_zmqprocess import ZMQProcess, MessageHandler, RequestProcessor, RequestErrorProcessor

sys.path.append(  os.path.abspath( os.path.join(curpath,"../../..")) )
from mod_repo import EntityStore, MongoEntityStore

import appsettings as CONST
from bson import json_util
import json

##########################################################################
# class: EntityRequestHandler
#   This class deals with how the server processes various entity requests
##########################################################################
class EntityRequestHandler(RequestErrorProcessor):
    def __init__(self, entityStore):

        if isinstance(entityStore, EntityStore):
            self.entityStore = entityStore
        else:
            raise AttributeError("entityStore needs to be an instance of EntityStore class")

    def handle_error(self, error, errorCode="500"):
        response = response = [errorCode, "Error", error]
        return response

    #######################################################################
    def createEntity(self, request):
        # print("SERVER: Processing CREATE request: %s" % request)

        try:
            if 'data' not in request:
                raise ValueError(' "data" needs to be part of CREATE request') 

            self.entityStore.addEntity( request["key"], request["data"])
            response = ["200", "Entity created"]
        except Exception as ex:
            response = ["500", "Error", str(ex)]

        return response

    #######################################################################
    def editEntity(self, request):
        # print("SERVER: Processing EDIT request: %s" % request)

        try:
            self.entityStore.editEntity( request["key"], request["data"])
            response = ["200", "Entity updated"]
        except Exception as ex:
            response = ["500", "Error", str(ex)]
            
        return response

    #######################################################################
    def getEntity(self, request):
        # print("SERVER: Processing GET request: %s" % request)

        try:
            entity = self.entityStore.getEntity( request["key"])
            entity = json.dumps(entity, default=json_util.default)
            response = ["200", "Success", entity]
        except ValueError as ex:
            response = ["404", "Invalid Key Error", str(ex)]
        except Exception as ex:
            response = ["500", "Error", str(ex)]
            
        return response

    #######################################################################
    def deleteEntity(self, request):
        # print("SERVER: Processing DELETE request: %s" % request)

        try:
            entity = self.entityStore.deleteEntity( request["key"])
            response = ["200", "Success"]
        except Exception as ex:
            response = ["500", "Error", str(ex)]
            
        return response

    #######################################################################
    def getEntityList(self, request):
        # print("SERVER: Processing GETLIST request: %s" % request)
        
        try:
            entities = self.entityStore.getEntitiesAsList()
            entities = json.dumps(entities, default=json_util.default)
            response = ["200", "Success", entities]
        except Exception as ex:
            response = ["500", "Error", str(ex)]

        return response                  
##########################################################################

##########################################################################
# class: EntityResponseStreamHandler
#   This class encapsulates the APIs that customer can access
#   Get called for each request, streams back a JSON response 
##########################################################################
class EntityResponseStreamHandler(MessageHandler):
    def __init__(self, responseStream, requestProcessor, stop, workerID=0):
        ''' 
            :param responseStream  : A callable JSON based ZMQ response stream
            :param requestProcessor: object that would provide APIs to handle operations
                                     that this class is expected to handle.
        '''           
        super(EntityResponseStreamHandler,self).__init__()

        self.responseStream = responseStream
        self.stop = stop
        self.workerID = workerID 
        self.requestProcessor = requestProcessor

    def sendJSONResponse(self,rep):
        rep.append("worker:%d"% self.workerID)
        print("Server response:",rep)
        self.responseStream.send_json(rep)

    def createEntity(self, data):
        rep = self.requestProcessor.createEntity(data)
        self.sendJSONResponse(rep)

    def editEntity(self, data):
        rep = self.requestProcessor.editEntity(data)
        self.sendJSONResponse(rep)

    def deleteEntity(self, data):
        rep = self.requestProcessor.deleteEntity(data)
        self.sendJSONResponse(rep)

    def getEntity(self, data):
        rep = self.requestProcessor.getEntity(data)
        self.sendJSONResponse(rep)

    def getEntityList(self, data):
        rep = self.requestProcessor.getEntityList(data)
        self.sendJSONResponse(rep)

    def handle_error(self, error, errorCode="500"):
        rep = [errorCode, "Error", error]
        self.sendJSONResponse(rep)

    def stopStream(self):
        if self.stop :
            self.stop()
##########################################################################

##########################################################################
# class: EntityAPI_ServerWorker
#   A basic API server built using ZMQProcess to handle CRUD requests 
##########################################################################
class EntityAPIWorker(ZMQProcess):
    ''' Server to handle pings '''
    def __init__(self, host= None, port = None, workerID = 0):
        super(EntityAPIWorker,self).__init__()

        self.reply_stream = None
        self.servHost = host
        self.servPort = port
        self.workerID = workerID

        # Create an instance of a class that implements RequestProcessor. 
        # Server will execute the processRequest function when it gets a message from client
        self.entityStore = MongoEntityStore(host= CONST.DB_SERVER, port= int(CONST.DB_PORT), database=CONST.DB_NAME, collection=CONST.DB_COLLECTION)
        self.requestHandler = EntityRequestHandler(self.entityStore)

    #############################################################
    def setup(self):
        super(EntityAPIWorker,self).setup()

        self.reply_stream, port = self.stream(sock_type = zmq.REP, addr= self.servHost, port = self.servPort, bind = False)

        responseStreamHandler  = EntityResponseStreamHandler(self.reply_stream, self.requestHandler, self.stop, workerID = self.workerID )
        self.reply_stream.on_recv(responseStreamHandler)

    #############################################################
    def run(self):
        ''' Initializes the event loop, creates the sockets/streams 
            and starts the (blocking) loop 
        '''
        
        self.setup()
        print("Started EntityAPIWorker process:%d"% self.workerID)
        try:
            # Start the loop. It runs until we stop it.
            self.loop.start()

        except KeyboardInterrupt: 
            print("EntityAPIWorker:%d received termination request"% self.workerID)
        except Exception as e:
            print("Error: %s" % str(e))    
        finally:
            self.stop()

    #############################################################
    def stop(self):
        ''' Stops the event loop. '''
        if self.reply_stream:
            self.reply_stream.flush()

        if self.loop:
            self.loop.stop()

        self.context.term()

        if self.requestHandler:
            self.requestHandler.stopStream()

        self.entityStore = None

        print("Terminated Worker:%d"% self.workerID)

####################### END of SIMPLE SERVER #############################
