# authmanager.py

import requests
from cork import Cork
from cork.backends import MongoDBBackend

import appconfig as CONF

class AuthFactory(object):
    
    def __init__(self):
        pass

    def initiate_authmgr(self):
        ''' Internal function to intiate authentication manager '''
        self.authBackend = MongoDBBackend (
            db_name=CONF.mongo_conf['db'], 
            hostname=CONF.mongo_conf['host'], 
            port=CONF.mongo_conf['port'], 
            initialize=False, 
            username=CONF.mongo_conf['username'], 
            password=CONF.mongo_conf['password'])

        smtp_url= CONF.smtp_url
        self.authmgr = Cork(backend= self.authBackend, 
            email_sender='bedabrata.chatterjee@gmail.com', 
            smtp_url=smtp_url)

        return self.authmgr