import os
import sys
import unittest
import datetime
import random

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curpath, '..')))

from mod_repo import MongoEntityStore

TEST_KEY = "testEntity%d" % random.randint(1,1000)
##################################################################
class MongoStoreTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MongoStoreTests, self).__init__(*args, **kwargs)

        # Setup the repo
        self.repo = MongoEntityStore(host='localhost', port=27017, database='testdb', collection='entities')
        
    ##################################################################
    def test1_AddEntity_expectnoerror(self):
        data = dict( type = 'testEntity')
        ent = self.repo.addEntity( key = TEST_KEY , data = data )
        self.assertIsNotNone(ent, 'addEntity should return an entity key' )

        findEntity = self.repo.getEntity(key = TEST_KEY)
        self.assertIsNotNone(findEntity, "We should find the added entity")

    ##################################################################
    def test2_EditEntity_expectnoerror(self):

        data = dict( type = 'testEntity' , modified = True)
        ret = self.repo.editEntity(key=TEST_KEY, data = data )
        self.assertTrue(ret, 'Edit api should return true') 

        findEntity = self.repo.getEntity(key = TEST_KEY)
        self.assertIsNotNone(findEntity, "We should find the added entity")
        self.assertIs(findEntity['data']['modified'], True, 'modified flag should be set as true')

    ##################################################################
    def test3_BulkEditEntity_expectnoerror(self):

        for i in range(5):
            data = dict( type = 'bulktestEntity', entry = i)
            testkey = "%s-bulk-test-%d" % (TEST_KEY, i)
            ent = self.repo.addEntity( key = testkey  , data = data )

        data = dict( type = 'bulktestEntity', modified = True)
        ret = self.repo.bulkEditEntity(
            cond={ "key": { "$regex": "%s-bulk-test" % TEST_KEY  }},
            updateStmt={ '$set' : { 'data': data } })

        self.assertEqual(ret, 5, 'Bulk Edit api should update 5 records') 

    ################################################################
    def test4_getEntitiesAsList_expectList(self):
        entities = self.repo.getEntitiesAsList(cond={ "key": { "$regex": "%s"  % TEST_KEY } })
        self.assertTrue( isinstance(entities, list) , 'getEntities should return a list of entities' )
        self.assertEqual(len(entities), 6, 'getEntities should return 6 records') 

    ##################################################################
    def test5_getEntitiesIterator_expectIterator(self):
        entities = self.repo.getEntities()
        self.assertTrue( hasattr(entities,'__iter__') , 'getEntities should return an iterator' )

    ##################################################################
    def test6_DeleteEntity_expectnoerror(self):
        ret = self.repo.deleteEntity(key=TEST_KEY)
        self.assertTrue(ret, 'Delete api should return true') 
        findEntity = self.repo.getEntity(key = TEST_KEY)
        self.assertIsNone(findEntity, "We should not find the deleted entity")

    ##################################################################
    def test7_BulkEditEntity_expectnoerror(self):
        ret = self.repo.bulkDeleteEntities(cond={ "key": { "$regex": "%s-bulk-test" % TEST_KEY  }})
        self.assertEqual(ret, 5, 'Bulk Delete api should have deleted 5 records') 
    #################################################################

##################################################################
if __name__ == '__main__':
    unittest.main()

