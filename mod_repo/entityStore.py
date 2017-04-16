from abc import ABCMeta
##########################################################################
# class: EntityStore
#   Base class for all entity stores implementing basic CRUD API
##########################################################################
class EntityStore(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        pass

    def addEntity(self,key, data):
        ''' add a new entity with the given key '''        
        pass

    def editEntity(self,key, data):
        ''' edit entity that matches the given key '''        
        pass

    def deleteEntity(self,key, data):
        ''' delete entity that matches the given key '''        
        pass

    def getEntity(self,key):
        ''' get entity that matches the given key '''
        pass


    def getEntities(self):
        ''' returns an iterator of entities '''
        pass

##########################################################################

##################################################################        
FILE_VERSION = "1.0.0"
if __name__ == '__main__':
    print("webinabottle:entitystore:%s" % FILE_VERSION)