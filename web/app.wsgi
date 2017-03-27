import os
import sys
import bottle
from bottle import *

from beaker.middleware import SessionMiddleware

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curpath)

app_root_path = os.path.abspath(curpath)
sys.path.append(app_root_path)

app_views_path = os.path.abspath( os.path.join(curpath,"./views/"))
bottle.TEMPLATE_PATH.insert(0, app_views_path )

import webconfig as CONF
import mod_foo
import mod_admin

from authmanager import AuthFactory 
authmgr = AuthFactory().initiate_authmgr()

bottle.BaseTemplate.defaults['URL_PREFIX'] = ''
application = bottle.default_app()

#######################################################################################
def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    print("\n Received %s:%s" % (username, password) )
    authmgr.login(username, password, success_redirect='/foo/index', fail_redirect='/login')

@bottle.route('/')
def index():
    """Only authenticated users can see this"""
    authmgr.require(fail_redirect='/login')
    # return 'Welcome! <a href="/admin">Admin page</a> <a href="/logout">Logout</a>'
    bottle.redirect("/foo/index")


@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    if authmgr.user_is_anonymous:
        return 'True'

    return 'False'

@bottle.route('/logout')
def logout():
    authmgr.logout(success_redirect='/login')

@bottle.get('/register')
def user_register():
    """Serve user registration form"""
    t = template('baseTemplate.tmpl', dict(
        pagelets=['_registeruser.tpl'],
        active_page='register',
        page_title= 'User Registration',
    ))
    return t

@bottle.post('/register')
def register():
    """Send out registration email"""
    authmgr.register(
        post_get('username'), 
        post_get('password'), 
        post_get('email_address'),
        email_template="registration_email.tpl"
    )
    return 'Please check your mailbox.'


@bottle.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    authmgr.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    authmgr.send_password_reset_email(
        username=post_get('username'),
        email_addr=post_get('email_address')
    )
    return 'Please check your mailbox.'


@bottle.route('/change_password/:reset_code')
@bottle.view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    authmgr.reset_password(post_get('reset_code'), post_get('password'))
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.route('/restricted_download')
def restricted_download():
    """Only authenticated users can download this file"""
    authmgr.require(fail_redirect='/login')
    return bottle.static_file('static_file', root='.')


@bottle.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    print("Session from WebInABottle: %s" % repr(session))
    authmgr.require(fail_redirect='/login')
    return authmgr.current_user.role

# Static pages
##########################################################################
@bottle.route('/login')
# @bottle.view('login')
def login_form():
    """Serve login form"""
    #t = template('login.tmpl', {'page_title': 'Login' })
    t = template('baseTemplate.tmpl', dict(
        pagelets=['_login.tpl'],
        active_page='login',    
        page_title= 'Login',
    ))
    return t


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'
################################################################################    
@error(404)
def error404(error):
    response.set_header('Content-type', 'text/html')
    return 'I do not know of this content'

@get('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root= os.path.join(curpath, 'static') )

#######################################################################################
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1337))
    application.mount(prefix='/foo/', app=mod_foo.foo)
    application.mount(prefix='/admin/',app=mod_admin.admin)
    
    application = SessionMiddleware(application,CONF.session_opts)
    bottle.run(app=application, host='0.0.0.0', port=port, debug=True, reloader=True)
    
