import os
import sys
import bottle
from bottle import *

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curpath)

app_root_path = os.path.abspath(curpath)
sys.path.append(app_root_path)

app_api_path = os.path.abspath( os.path.join(curpath, "../api"))
sys.path.append( app_api_path )

bottle.BaseTemplate.defaults['URL_PREFIX'] = ''

application = bottle.default_app()

import mod_foo
application.mount(prefix='/foo/', app=mod_foo.foo_controller)

@error(404)
def error404(error):
    response.set_header('Content-type', 'text/html')
    return 'I do not know of this content'

@get('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root= os.path.join(curpath, 'static') )
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1337))
    run(host='0.0.0.0', port=port, debug=True, reloader=True)
