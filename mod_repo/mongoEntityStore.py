import datetime
import pymongo
from pymongo import MongoClient
from entityStore import EntityStore

#################################################################################
# class: MongoEntityStore
#   Concrete class for entity implemented using MongoDB (pyMongo 3.4 required)
#################################################################################
class MongoEntityStore(EntityStore):
    def __init__(self, host='localhost', port=27017, database='testdb', collection='entities', debug=False):
        ''' The constructor for MongoEntityStore needs the following parameters: 
        :param host - address of the MongoDB server (defaulted to localhost)
        :param port - port of the MongoDB server (defaulted to 27017)
        :param database   - name of the database (defaulted to 'testdb')
        :param collection   - name of the collection used to store entity (defaulted to 'entities')
        '''
        self.client = MongoClient(host, port)
        self.db = self.client[database]
        self.collection = self.db[collection]
        self.DEBUG_MODE = debug

    ##################################################################
    def addEntity(self,key, data):

        if (not key) or (not data):
            raise ValueError("key and data need to be specified for insert api")   

        rec = self.collection.find_one({'key': key})
        if rec:
            print rec
            raise ValueError("Key already exist. Please use update API")

        recid = self.collection.insert_one({'key': key, 'data': data , 'timestamp': datetime.datetime.utcnow() }).inserted_id
        
        if self.DEBUG_MODE:
            print("Added record with key: %s" % key)

        return recid

    ##################################################################
    def editEntity(self,key, data, upsert=False):

        if (not key) or (not data):
            raise ValueError("key and data need to be specified for the edit api")  

        if self.DEBUG_MODE:
            print("Searching for key: %s" % key)
        
        rec = self.collection.find_one({'key': key})
        if not rec:
            raise ValueError("Key does not exist.")
        self.collection.replace_one({'_id': rec['_id']}, { 'key': key, 'data': data , 'timestamp': datetime.datetime.utcnow() })
        
        if self.DEBUG_MODE:
            print("Added record with key: %s" % key)
        
        return True

    ##################################################################
    def bulkEditEntity(self,cond=None, updateStmt = {}):
        ''' api to bulk edit entities. cond needs to be specified 
            param:  cond : filter condition
            param:  updateStmt : mongo specific update condition     
            returns the number of records that matched the filter condition
        '''
        if not cond:
            raise ValueError('cond needs to be specified for bulk delete api')

        result = self.collection.update_many(cond, updateStmt)
        return result.matched_count

    ##################################################################
    def deleteEntity(self,key=None):
        
        if not key:
            raise ValueError("key need to be specified for delete api")    

        if self.DEBUG_MODE:
            print("Searching for key: %s" % key)

        rec = self.collection.find_one({'key': key})

        if not rec:
            raise ValueError("Key not present. Item needs to exist to be deleted")        
        
        self.collection.delete_one({'key': key})

        if self.DEBUG_MODE:
            print("Deleted record with for key: %s" % key)

        return True

    ##################################################################
    def bulkDeleteEntities(self,cond=None):
        ''' api to delete entities. cond needs to be specified '''

        if not cond:
            raise ValueError('cond needs to be specified for bulk delete api')
        ret = self.collection.delete_many(cond)

        return ret.deleted_count

    ##################################################################
    def getEntity(self,key):
        ''' api to retrieve element based on a key. May return None in case key is not present '''
        if not key:
            raise ValueError("key need to be specified for get api")   

        projection = {'_id':0, 'timestamp': 0  }
        rec = self.collection.find_one( {'key': key}, projection)
        return rec

    ##################################################################
    def getEntityByID(self,recid=None):
        ''' api to retrieve an entity based on mongo _id '''
        if not recid:
            raise ValueError("recid need to be specified for get api")   

        projection = {'_id':0, 'timestamp': 0  }
        rec = self.collection.find_one({'_id': recid}, projection )

        if not rec:
            raise ValueError("Record does not exist.")
        return rec

    ##################################################################
    def getEntities(self, cond = {}):
        ''' Returns a python iterator '''
        projection = {'_id':0, 'timestamp': 0  }
        for rec in self.collection.find(cond, projection):
            yield rec

    ##################################################################
    def getEntitiesAsList(self, cond = {}):
        
        projection = {'_id':0, 'timestamp': 0  }
        recList =  [rec for rec in self.collection.find(cond, projection)]

        if self.DEBUG_MODE:
            print ("\n List of Entities: %s" % recList)

        return recList

##################################################################        
FILE_VERSION = "1.0.0"
if __name__ == '__main__':
    print("webinabottle:MongoEntitystore:%s" % FILE_VERSION)