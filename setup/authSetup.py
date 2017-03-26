# authSetup.py
import os
import sys
from cork import Cork
from cork.backends import MongoDBBackend


curpath = os.path.dirname(os.path.abspath(__file__))
app_api_path = os.path.abspath( os.path.join(curpath, "../api/"))
sys.path.append( app_api_path )

import appconfig as CONF

mb = MongoDBBackend (db_name=CONF.mongo_conf['db'], 
        hostname=CONF.mongo_conf['host'], 
        port=CONF.mongo_conf['port'], 
        initialize=True,
        username=CONF.mongo_conf['username'], 
        password=CONF.mongo_conf['password'])

smtp_url= CONF.smtp_url

aaa = Cork(backend= mb, 
            email_sender='admin@webinabottle.com', 
            smtp_url=smtp_url)

################################################################################
def create_roles():
    ''' Create basic application roles '''
    print("Creating roles")
    mb.roles._coll.insert({'role': 'admin', 'val': 100})
    mb.roles._coll.insert({'role': 'user', 'val': 50})
################################################################################
def createAdminUser():
    ''' Create Admin user account '''
    # Note: First create a regular user and then uses a hash value for the admin account
    print("Creating Admin user")
    mb.users._coll.insert({
        "login": "admin",
        "email_addr": "admin@webinabottle.com",
        "desc": "admin test user",
        "role": "admin",
        "hash": "cPApoAKWE4/AhPJmolLVqyXPWktCZgKA88eNI6upWakXDbu/S2l4VikzKbw5qh/Et8JQsMYDf+rZsmobXL2hCmg=",
        "creation_date": "2017-03-25 00:00:00.000000"
    })
################################################################################
def registerUsers():
    ''' Initiate a register user flow '''
    print("Registering users")
    email_template = os.path.abspath( os.path.join(curpath, "../web/views/registration_email.tpl"))
    aaa.register('bbc','bbc@123','bedabrata.chatterjee@gmail.com',email_template=email_template)    
    print("User registration initiated. Please check your email")
################################################################################


if __name__ == "__main__":
    print("Initiating Mongo based Authentication setup for WebInABottle application")
    create_roles()
    registerUsers()
    print("Authentication setup complete.")
