# Web in a Bottle 
This is a simple application build to serve as a boilerplate Bottle application.

It uses the following framework/packages/library

+ Python 
+ MongoDB 
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
## How to run the application server

$ python web/app.wsgi

This starts standalone WSGI server that is listening to port 1337

Point your browser to localhost:1337
