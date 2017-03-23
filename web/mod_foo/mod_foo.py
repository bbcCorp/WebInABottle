import os
import sys
import bottle
from bottle import *

foo_controller = Bottle()

curpath = os.path.dirname(os.path.abspath(__file__))
app_views_path = os.path.abspath( os.path.join(curpath,"../views/"))
bottle.TEMPLATE_PATH.insert(0, app_views_path )

#######################################################################
@route("/")
@route("/", method = "POST")
def foo_index():
    response.set_header('Content-type', 'text/html')
    t = template('app_main.tmpl', { 
        'page_title': "Web in a Bottle", 
        'page_header': 'List of Application Functionalities',
        'contentLst' : ["Function #1", "Function #2", "Function #3"] 
    })
    # t = template('app_main.tmpl')
    return t

#######################################################################    