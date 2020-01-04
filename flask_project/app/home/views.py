# coding='utf-8'
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegisterForm, LoginForm
from app.models import User, Userlog
from werkzeug.security import generate_password_hash
from app import db
import uuid, time
from functools import wraps


# 会员登录装饰器.会员中心访问需要
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@home.route("/")
def index():
    return render_template("home/index.html")


# 登录
@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_pwd(data['pwd']):
            flash("密码错误！", 'err')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('home/login.html', form=form)


# 退出
@home.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))  # 蓝图名.函数名


# 注册
@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！", 'ok')
        time.sleep(2)
        return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 会员中心
@home.route('/user/')
@user_login_req
def user():
    return render_template('home/user.html')


# 修改密码
@home.route('/pwd/')
@user_login_req
def pwd():
    return render_template('home/pwd.html')


# 评论
@home.route('/comments/')
@user_login_req
def comments():
    return render_template('home/comments.html')


# 登录日志
@home.route('/loginlog/')
@user_login_req
def loginlog():
    return render_template('home/loginlog.html')


# 收藏
@home.route('/moviecol/')
@user_login_req
def moviecol():
    return render_template('home/moviecol.html')


# 轮播图
@home.route('/animation/')
def animation():
    return render_template('home/animation.html')


# 搜索
@home.route('/search/')
def search():
    return render_template('home/search.html')


# 视频播放
@home.route('/play/')
def play():
    return render_template('home/play.html')
