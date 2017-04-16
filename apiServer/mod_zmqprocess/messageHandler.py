from zmq.utils import jsonapi as json

##########################################################################
class MessageHandler(object):
    '''Base class for message handlers for a ZMQProcess'''
    def __init__(self, json_load=-1):
        self._json_load = json_load

    def __call__(self, msg):
        '''
            Gets called when a messages is received by the stream this handlers is registered at

            *msg* is a list as return by zmq.core.socket.Socket.recv_multipart
        '''

        
        i = self._json_load
        msg_type, data = json.loads(msg[i])
        msg[i] = data

        # print ("\n\n msgType:%s \n data:%s" % (msg_type, data))
        
        # Get the actual message handler and call it
        if msg_type.startswith('_'):
            raise AttributeError('%s starts with an "_"' % msg_type)

        if not hasattr(self, msg_type):
            args = ["Invalid API" , "403"]
            getattr(self, 'handle_error')( *args )
        else:
            # now call self.msg_type(msg)
            getattr(self, msg_type)(*msg)


##########################################################################
class RequestProcessor(object):
    def processRequest(self, request):
        ''' process request and send back a JSON response '''
        response = 'Processed request'
        return response
##########################################################################
class RequestErrorProcessor(object):
    def handle_error(self, error, errorCode):
        response = str(error)
        return response

##########################################################################        