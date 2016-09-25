# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, abort, flash, g
from flask_login import LoginManager, UserMixin, logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm
from app import dbhelper, rconfile, app
import json

def is_valid_time(int):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.localtime(int)
    return True
  except:
    return False
    
def all_lower(L):
    '''把字符串转为小写'''
    if (isinstance(L, int)):
        L = str(L)
    return [s.lower() for s in L]

class User(UserMixin):
    def __init__(self, username, password = ''):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(users[self.username]['pw'])

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
#    def is_authenticated(self):
#        return True
#    def is_active(self):
#        return True
#    def is_anonymous(self):
#        return False
#    def get_id(self):
#        try:
#            return unicode(self.id)  # python 2
#        except NameError:
#            return str(self.id)  # python 3

def prn_obj(obj):
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])
            
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
#login_manager.login_view = "login"
db = dbhelper.DBHelper()
hostlist = rconfile.readconfigfile()
hostlist_lower = all_lower(hostlist)
users = {'admin': {'pw': 'admin'}}    

'''登录前检测'''
@app.before_request
def before_request():
    #print current_user.is_authenticated
    #prn_obj(current_user)
    g.user = current_user
    #print g.user.is_authenticated
    #prn_obj(g.user)
    

'''用户回调'''
@login_manager.user_loader
def load_user(username):
    if username not in users:
        return

    user = User(username)
    user.id = username
    return user

#'''请求'''
#@login_manager.request_loader
#def request_loader(request):
#    username = request.form.get('UserName')
#    if username not in users:
#        return
#    user = User()
#    user.id = username
#    return user
    
#'''请求'''
#@login_manager.request_loader
#def request_loader(request):
#    username = request.form.get('UserName')
#    if username not in users:
#        return
#    user = User()
#    user.id = username
#    #user.is_authenticated = request.form['Password'] == users[username]['pw']
#    return user

'''未认证'''
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/login')

'''404页面'''
@app.errorhandler(404)
@login_required
def page_not_found(error):
    return render_template('404.html'), 404

'''登录页面'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
    message =u'''
        <div class="alert alert-dismissable alert-danger">
             <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
            <h4>
                登录失败！
            </h4>
            <div>
                请检查用户名和密码。
            </div>
        </div>
        '''
    #g.user = current_user
    #if current_user is not None: #and current_user.is_authenticated:
    #    return redirect('/')
    #print g.user
    #if g.user == 'admin':
    #     return redirect('/')
    if g.user != None and g.user.is_authenticated:
        return redirect(url_for('index'))
    #else:
    #    print 2
    if request.method == 'GET':
        return render_template('login.html')
    try:
        username = request.form['UserName']
        passwd = request.form['Password']
    except AttributeError:
        return render_template('login.html',message = message)
    if username in users:
        user = User(username,passwd)
        if user.check_password(passwd):
            user.id = username
            login_user(user)
            return redirect('/')

    return render_template('login.html',message = message)
        
'''
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in successfully.')
        return redirect('/')
    return render_template('login.html',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
'''

'''json接口（主机列表）'''
@app.route('/enzf/hostlist',methods=["GET"])
@login_required
def enzfHost():
    return json.dumps(hostlist)

'''主页'''
@app.route('/')
@login_required
def index():
    return render_template('index.html')

'''json接口（数据库）'''
'''搜索后面不能带空格BUG未解决'''
@app.route('/enzfdata',methods=["GET"])
@login_required
def datahelper():
    try:
        tmp_time = int(request.args.get('time'))
        tmp_host = str(request.args.get('host')).lower().strip()
    except (TypeError,ValueError):
        return abort(404)
    if tmp_host == 'total' or tmp_host in hostlist_lower:
        if str(tmp_time).isdigit():
            resu = db.smartselect(tmp_time, tmp_host)
            return json.dumps(resu)
    else:
        print 'Block attack!'
        return abort(404)

'''英文征服监控页面'''
@app.route('/enzf/<host>')
@login_required
def hostonline(host):
    host = str(host)
    if host.lower() == 'total' or host.lower() in hostlist_lower:
        return render_template('enzf.html')
    else:
        abort(404)

'''仪表板'''
@app.route('/panel')
@login_required
def plan():
    return render_template('panel.html')

'''关于'''
@app.route('/about')
@login_required
def about():
    return render_template('about.html')

'''页面不存在'''
@app.route('/pnf')
@login_required
def pnf():
    return render_template('404.html')

'''注销'''
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
    
@app.route('/favicon.ico')
def inco():
    return url_for('static', filename='favicon.ico')