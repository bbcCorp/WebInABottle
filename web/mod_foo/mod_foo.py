import os
import sys
import bottle
from bottle import *

foo_controller = Bottle()

curpath = os.path.dirname(os.path.abspath(__file__))
app_views_path = os.path.abspath( os.path.join(curpath,"../views/"))
bottle.TEMPLATE_PATH.insert(0, app_views_path )


app_api_path = os.path.abspath( os.path.join(curpath, "../../api"))
sys.path.append( app_api_path )
from foomanager import FooManager

#######################################################################
@route("/")
@route("/", method = "POST")
def foo_index():
    response.set_header('Content-type', 'text/html')

    fm = FooManager()
    data = fm.getInfo()
    t = template('app_main.tmpl', { 
        'page_title': "Web in a Bottle", 
        'page_header': 'List of Application Functionalities',
        'contentLst' :  data
    })
    # t = template('app_main.tmpl')
    return t

#######################################################################    