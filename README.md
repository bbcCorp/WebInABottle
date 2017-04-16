# Web in a Bottle 

This is a sample application build to serve as a boilerplate Bottle application. However unlike other sample applications, these goes a extra steps to demostrate how to build a scalable microservice architecture to seperate out various components that would otherwise be closely tied up in a monolithic application.

1. It uses a microservice architecture for its sample api. Web server does not know anything about how the data apis are served and stored. There is an external apiServer which handles that concern. The apiService is built using ZeroMQ and uses a multiprocessor architecture to host the service. 

2. The web server connects to the apiServer to get its data. This allows having multiple versions of apiServer running parallelly or swapping out one service with another without affecting the web server.

3. A nearly complete user registration and login mechanism implemented using bottle-cork. Just plug in SMTP server configuration to get user registration emails.  

Dependencies
==============
It uses the following framework/packages/library

+ Python 
+ MongoDB and pyMongo (3.4.0)
+ ZeroMQ and pyzmq
+ <a href="http://bottlepy.org/docs/dev/index.html" title="Python Bottle">Bottle web framework</a> and the <a href="http://bottlepy.org/docs/dev/stpl.html" title="SimpleTemplate Engine">SimpleTemplate Engine</a> 
+ Bootstrap and the <a href="https://bootswatch.com/yeti/" title="Bootswatch Yeti">Bootswatch Yeti</a>
+ jQuery 
+ FontAwesome
+ <a href="https://github.com/FedericoCeratto/bottle-cork" title="Bottle-Cork">Bottle-Cork</a> for authentication and authorization
------------------------------------------------------
## Application Setup

+ Make sure the python dependencies and MongoDB is installed. Check out the scripts in the setup directory
+ Update the application configuration file:  api/appconfig.py
+ Update the file setup/authSetup.py with your credentials and execute the script

------------------------------------------------------
## Running the apiServer
To start the apiServer use the following command. This will start a ZMQ-based server with 2 worker nodes listening to port 7000

$ python apiServer/runServer.py

------------------------------------------------------
## How to run the application server

$ python web/app.wsgi

This starts standalone WSGI server that is listening to port 1337

Point your browser to localhost:1337

------------------------------------------------------
