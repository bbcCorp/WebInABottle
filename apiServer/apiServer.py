import zmq
from zmq.devices import ProcessDevice
import multiprocessing
import appsettings as CONST
from apiWorker import EntityAPIWorker

class EntityAPIServer(multiprocessing.Process):
    ''' EntityAPIServer implementation as a Queue with multiple backend services'''

    def __init__(self):
        super(EntityAPIServer,self).__init__()

        self.processDevice = None
        self.workers = []
        pass

    def setup(self):
        ''' Setup the necessary infrastructure for the server '''
        self.__setupQueueProcess()
        self.__setupWorkers()

    def __setupQueueProcess(self):
        ''' Set up a zmq Queue ProcessDevice '''
        self.processDevice = ProcessDevice(zmq.QUEUE, zmq.XREP, zmq.XREQ)
        self.processDevice.bind_in("%s://%s:%s" % (CONST.FRONTEND_SOCKET["proto"],CONST.FRONTEND_SOCKET["addr"],CONST.FRONTEND_SOCKET["port"]))
        self.processDevice.bind_out("%s://%s:%s" % (CONST.SERVICE_SOCKET["proto"],CONST.SERVICE_SOCKET["addr"],CONST.SERVICE_SOCKET["port"]))
        self.processDevice.setsockopt_in(zmq.IDENTITY, 'ROUTER')
        self.processDevice.setsockopt_out(zmq.IDENTITY, 'DEALER')

    def __setupWorkers(self):
        ''' Setup N workers depending on the application configuration '''
        
        for i in range(CONST.WORKER_SERVICES_COUNT):
            print("Creating worker process:%d"% (i+1))
            workerProc = EntityAPIWorker (host= CONST.SERVICE_SOCKET["addr"], port = CONST.SERVICE_SOCKET["port"] , workerID = i+1 )
            self.workers.append(workerProc)

    def run(self):
        self.setup()

        print("Initiating Queue")
        self.processDevice.start()

        print("Starting Workers")
        for worker in self.workers:
            worker.start()

        for worker in self.workers:
            worker.join()

    def stop(self):

        if self.workers:
            for worker in self.workers:
                worker.stop()