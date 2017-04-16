import multiprocessing
import zmq
from zmq.eventloop import ioloop, zmqstream

##########################################################################
# class: ZMQProcess
#   Base class for setting up a stream based asynchronous ZMQ Connection
##########################################################################
class ZMQProcess(multiprocessing.Process):

    def __init__(self):
        super(ZMQProcess,self).__init__()
        self.loop = None
        self.context = None

    #############################################################
    def setup(self):
        self.context = zmq.Context()
        self.loop = ioloop.IOLoop.instance()

    #############################################################
    def stream(self, sock_type = zmq.REP, addr=None, port=None, bind = False, callback=None, subscribe=None):
        ''' Creates a "zmq.eventloop.zmqstream.ZMQStream 
            :param sock_type: The ZMQ socket type (e.g. zmq.REQ)
            :param addr: Address to bind or connect to. Just mention the address or IP *WITHOUT* protocol or PORT
            :param port: Port number to bind or connect / None (bind to random port)
            :param bind: Binds to *addr* if True or tries to connect to it otherwise.   
            :param callback: A callback for zmq.eventloop.zmqstream.ZMQStream.on_recv (optional)
            :param subscribe: Subscription pattern for *SUB* sockets (optional)

            :returns: A tuple containg the stream and the port number.
        '''

        sock = self.context.socket(sock_type)

        if bind:
            if port:
                sock.bind( "tcp://%s:%s" % (addr, port))
            else:
                port = sock.bind_to_random_port('tcp://%s' % (addr))
        
        else:
            if (not addr) or (not port):
                raise ValueError("Address and Port parameters are mandatory to CONNECT to a server")
                
            sock.connect("tcp://%s:%s" % (addr, port))

        # Add a default subscription for SUB sockets
        if sock_type == zmq.SUB:
            if subscribe:
                sock.setsockopt(zmq.SUBSCRIBE, subscribe)

        # We need to create a stream from our socket and # register a callback for recv events.
        stream = zmqstream.ZMQStream(sock , self.loop) 

        if callback:
            stream.on_recv(callback)

        return stream, int(port)


########################### End of ZMQBaseConnection ###############################################