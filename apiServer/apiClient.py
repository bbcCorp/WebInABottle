import multiprocessing
import zmq
import time
import random

##########################################################################
# class: EntityAPIClient
#   A basic client that sends a ping to a server and processes a response
##########################################################################
class EntityAPIClient(multiprocessing.Process):
    
    ''' Client to ping the server '''
    def __init__(self, serverHost = None, serverPort = "80", clientID=0):
        super(EntityAPIClient,self).__init__()
        self.msgCounter = 0
        self.clientID = clientID

        self.context = None
        self.clientSock = None
        self.serverAddr = "tcp://%s:%s" % (serverHost, serverPort)

    #############################################################
    def setup(self):
        self.context = zmq.Context()
        self.clientSock = self.context.socket(zmq.REQ)
        self.clientSock.connect(self.serverAddr)
    
    #############################################################
    def makeRequest(self,request):
        self.clientSock.send_json(request)
                
        msg = self.clientSock.recv()
        print (" CLIENT#%s: Response from server: %s\n" % (self.clientID, msg))
        # time.sleep( random.randint(0,5) )      # sleep for 0-5 sec between requests

    def run(self):
        ''' Initializes the event loop, creates the sockets/streams and starts the (blocking) loop '''
        
        self.setup()
        print("Started Client#%s process"% self.clientID)
        try:
            while True:
                self.msgCounter += 1

                # request = [ "invalidTest",  dict()]
                # self.makeRequest(request)

                # Put in a Create request
                requestKey = str(random.randint(1,1000))
                print ("\n CLIENT#%s: Create Entity:%s" %(self.clientID, requestKey))
                request = [ "createEntity",  dict( key = requestKey, data = dict( client = self.clientID, requestID = self.msgCounter ))]
                self.makeRequest(request)

                # Put in a get request
                print ("\n CLIENT#%s: Get Entity:%s" %(self.clientID, requestKey))
                request = [ "getEntity",  dict( key = requestKey )]
                self.makeRequest(request)

                # Put in a Edit request
                print ("\n CLIENT#%s: Edit Entity:%s" %(self.clientID, requestKey))
                request = [ "editEntity",  dict( key = requestKey , data = dict( client = self.clientID, requestID = self.msgCounter, edited = True ))]
                self.makeRequest(request)

                # Put in a Get request
                print ("\n CLIENT#%s: Get Entity:%s" %(self.clientID, requestKey))
                request = ["getEntity",  dict( key = requestKey )]
                self.makeRequest(request)

                # Put in a delete request
                print ("\n CLIENT#%s: Delete Entity:%s" %(self.clientID, requestKey))
                request = ["deleteEntity",  dict( key = requestKey )]
                self.makeRequest(request)

                # Put in a get request
                print ("\n CLIENT#%s: Get Entity List" %(self.clientID))
                request = [ "getEntityList",  dict()]
                self.makeRequest(request)

        except KeyboardInterrupt: 
            pass
        except Exception as e:
            print("Error: %s" % str(e)) 
        finally:            
            self.clientSock.close()
            self.context.term()
            print("Closed Client:%s socket"% self.clientID)

    #############################################################
    def stop(self):
            self.clientSock.close()
            self. context.term()
            print("Closed Client:%s socket"% self.clientID)

####################### END of SIMPLE CLIENT #####################################    