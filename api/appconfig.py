import os

mongo_conf = {
    'host' : os.environ['MONGO_SERVER'] if 'MONGO_SERVER' in os.environ else 'localhost',
    'port' : int(os.environ['MONGO_PORT']) if 'MONGO_PORT' in os.environ else 27017,
    'db' : 'webinabottle',
    'username': None,
    'password': None
}

smtp_url = 'starttls://yourGmailUsername:yourGmailPassword@smtp.gmail.com:587'
