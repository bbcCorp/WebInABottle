# run.py
import time
import multiprocessing
from apiServer import EntityAPIServer
import appsettings as CONST

def initialize():
    ''' Start the API Server using the specified configuration '''
    addr = CONST.FRONTEND_SOCKET["addr"]
    port = CONST.FRONTEND_SOCKET["port"]
    procs = []
    try:
        serverProc = EntityAPIServer()
        serverProc.start()
        procs.append(serverProc)
        
        for proc in procs:
            proc.join()
    
    except KeyboardInterrupt: 
        print("Stopping API Server")
    except Exception as ex: 
        print("Exception: ", str(ex))
    finally:
        for proc in procs:
            proc.stop()    

############################ MAIN PROGRAM #################################
if __name__ == "__main__":
    initialize()
########################### THE END ##################################