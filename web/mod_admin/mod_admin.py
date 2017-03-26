import os
import sys
import bottle
from bottle import *
import appconfig as CONF

admin = Bottle()

curpath = os.path.dirname(os.path.abspath(__file__))
app_views_path = os.path.abspath( os.path.join(curpath,"../views/"))
bottle.TEMPLATE_PATH.insert(0, app_views_path )

app_api_path = os.path.abspath( os.path.join(curpath, "../../api"))
sys.path.append( app_api_path )

from authmanager import AuthFactory 
authmgr = AuthFactory().initiate_authmgr()

####################################################################################

def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


##########################################################################
# Admin-only pages
##########################################################################
@admin.route('/')
@admin.route('/admin')
def index():
    """Only admin users can see this"""
    authmgr.require(role='admin', fail_redirect='/sorry_page')

    ## TODO: Create Admin views 
    t = template('admin.tmpl', dict(
        active_page="admin",
        page_title = "Web in a Bottle", 
        page_header = 'Administration',
        current_user=authmgr.current_user,
        users=authmgr.list_users(),
        roles=authmgr.list_roles()
    ))
    return t

@admin.post('/create_user')
def create_user():
    try:
        authmgr.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@admin.post('/delete_user')
def delete_user():
    try:
        authmgr.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception as e:
        print (repr(e))
        return dict(ok=False, msg=e.message)


@admin.post('/create_role')
def create_role():
    try:
        authmgr.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@admin.post('/delete_role')
def delete_role():
    try:
        authmgr.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)

####################################################################################