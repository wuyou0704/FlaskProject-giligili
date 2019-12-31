目录：

- [前台界面搭建](#前台界面搭建)
  - [路由](#路由)
  - [模板](#模板)
- [404页面搭建](#404页面搭建)
- [管理员页面搭建](#管理员页面搭建)
  - [路由](#路由)
  - [模板](#模板)
- [管理员登录和访问控制](#管理员登录和访问控制)
  - [表单验证](#表单验证)
  - [登出功能](#登出功能)
  - [访问控制](#访问控制)

### 前台界面搭建
#### 路由
在视图文件 app/home/views.py 注册相应路由：

``` python
@home.route("/")
def index():
    return render_template("home/index.html")


# 登录
@home.route('/login/')
def login():
    return render_template('home/login.html')


# 退出
@home.route('/logout/')
def logout():
    return redirect(url_for('home.login'))  # 蓝图名.函数名


# 注册
@home.route('/register/')
def register():
    return render_template('home/register.html')
    
......
```

#### 模板
模板路径：app/templates/home/

    ├── comments.html  会员-评论记录
    ├── home.html  网站导航和底部内容
    ├── index.html  电影列表页
    ├── login.html  登录
    ├── loginlog.html  会员-登录日志
    ├── menu.html  会员中心侧边导航
    ├── moviecol.html  会员-收藏电影
    ├── pwd.html  会员-修改密码
    ├── register.html  注册
    ├── user.html  会员-会员中心
    ├── animation.html  实现轮播图
    ├── index.html  存放电影标签、电影列表
    ├── layout.html  导航和底部内容，与 home.html 几乎一样(内容部分少了一个style)
    └── play.html  电影播放页面

做好的图：

![](http://www.gtfly.top:81/201912282206.png)

![](http://www.gtfly.top:81/201912282208.png)

![](http://www.gtfly.top:81/201912282209.png)

需要注意的点：

1.home.html 主要用来存放页面的导航和底部内容；因为登录和注册、会员等页面公共部分都有导航和底部内容，因此先将公共的部分写到 home.html 中，其他页面再来继承这个模板即可

2.要弄清楚页面的逻辑：点击退出按钮时，应该跳转到登录页面；在登录/注册页面点击登录/注册按钮时，验证成功后应该跳转到会员页面

3.menu.html 主要用来存放会员信息的侧边导航内容，里面的页面如：会员中心、修改密码等页面将其包含，并继承 home.html

4.会员信息需要修改css激活方式：

当点击会员中心时，蓝色光标需要移动到会员中心一栏：

![](http://www.gtfly.top:81/201912282232.png)

点击修改密码时，蓝色光标需要移动到修改密码一栏：

![](http://www.gtfly.top:81/201912282233.png)

...


浏览器显示的侧边栏的静态页面为：

    <div class="container" style="margin-top:76px">
        <div class="col-md-3">
            <div class="list-group">
                <a href="user.html" class="list-group-item active">
                    <span class="glyphicon glyphicon-user"></span>&nbsp;会员中心
                </a>
                 <a href="pwd.html" class="list-group-item">
                    <span class="glyphicon glyphicon-lock"></span>&nbsp;修改密码
                </a>
                <a href="comments.html" class="list-group-item">
                    <span class="glyphicon glyphicon-comment"></span>&nbsp;评论记录
                </a>
                <a href="loginlog.html" class="list-group-item">
                    <span class="glyphicon glyphicon-calendar"></span>&nbsp;登录日志
                </a>
                <a href="moviecol.html" class="list-group-item">
                    <span class="glyphicon glyphicon-heart"></span>&nbsp;收藏电影
                </a>
            </div>
        </div>

在项目中，需要将该静态css active选择器改为动态的，这里用jquery实现：

首先将每一个选项用id命名：

    <div class="col-md-3">
        <div class="list-group">
            <a id="m1" href="{{ url_for('home.user') }}" class="list-group-item">
                <span class="glyphicon glyphicon-user"></span>&nbsp;会员中心
            </a>
            <a id="m2" href="{{ url_for('home.pwd') }}" class="list-group-item">
                <span class="glyphicon glyphicon-lock"></span>&nbsp;修改密码
            </a>
            <a id="m3" href="{{ url_for('home.comments') }}" class="list-group-item">
                <span class="glyphicon glyphicon-comment"></span>&nbsp;评论记录
            </a>
            <a id="m4" href="{{ url_for('home.loginlog') }}" class="list-group-item">
                <span class="glyphicon glyphicon-calendar"></span>&nbsp;登录日志
            </a>
            <a id="m5" href="{{ url_for('home.moviecol') }}" class="list-group-item">
                <span class="glyphicon glyphicon-heart"></span>&nbsp;收藏电影
            </a>
        </div>
    </div>


然后在 home.html中定义模板js

最后在每一个页面实现写入jQuery，当点击id名对应的选项时，会将active属性添加到class中：

    {% block js %}
    <script>
        $(document).ready(function(){
            $("#m1").addClass("active");
        });
    </script>
    {% endblock %}

5.要注意会员信息页面例如 user.html 继承 home.html 与包含 menu.html 的逻辑，应该在基承块中包含，这样才能正确渲染

6.跳转页面所用方式是 url_for() ，参数格式是：蓝图名.方法名

7.index.html 继承 layout.html

8.模板中重复的部分可用循环来替代：

	{% for v in range(1, 13) %}
	...
	{% endfor %}

### 404页面搭建
使用flask函数：

    errorhandler(code_or_exception):用来监听捕捉异常,然后返回自定义的页面处理
    参数：code_or_exception – HTTP的错误状态码或指定异常

在Flask对象上注册此错误处理视图：

``` python
# 404错误处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404   # 返回404模板页面和状态码
```

### 管理员页面搭建
#### 路由

在视图文件 app/admin/views.py 注册相应路由

``` python
@admin.route("/login/")
def login():
    return render_template('admin/login.html')


@admin.route("/logout/")
def logout():
    return redirect(url_for('admin.login'))

......
```

#### 模板
路径：app/templates/admin/

    ├── admin_add.html  管理员管理-添加管理员
    ├── admin.html  管理员页面顶部导航和底部
    ├── admin_list.html  管理员管理-管理员列表
    ├── adminloginlog_list.html
    ├── auth_add.html  权限列表-添加权限
    ├── auth_list.html  权限管理-权限列表
    ├── comment_list.html  评论管理-评论列表
    ├── grid.html  管理员页面左侧菜单
    ├── index.html  首页-控制面板
    ├── login.html  管理员登录页面
    ├── movie_add.html    电影管理-电影列表
    ├── moviecol_list.html  收藏管理-收藏列表
    ├── movie_list.html  电影管理-电影列表
    ├── oplog_list.html  日志管理-操作日志列表
    ├── preview_add.html  预告管理-添加预告
    ├── preview_list.html  预告管理-预告列表
    ├── pwd.html  修改密码
    ├── role_add.html  角色管理-添加角色
    ├── role_list.html  角色管理-角色列表
    ├── tag_add.html  标签管理-添加标签
    ├── tag_list.html  标签管理-标签列表
    ├── user_list.html  会员管理-会员列表
    ├── userloginlog_list.html  日志管理-会员登录日志列表
    └── user_view.html  会员管理-会员列表-查看会员

1.类似前台页面搭建，grid.html 中存放侧栏菜单，admin.html 存放导航和底部内容，将grid.html 包含了进来；admin.html 还定义了css、js、以及网站内容的block，其他页面只需继承该模板即可


2.登录登出逻辑关系为点击登出要跳转到登录页面，因此只需一个登录模板即可

搭建好的页面：

![](http://www.gtfly.top:81/201912291513.png)



### 管理员登录和访问控制
#### 表单验证
需要使用Flask-WTF扩展

1.因为是多用户验证登录，所以需要用到数据库，因此首先在 app/models.py 中定义管理员数据库模型Admin，并插入一条管理员账号数据

2.在 app/admin/forms.py 中设置表单，首先要把表单定义为类：

``` python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin

# 管理员登录表单
class LoginForm(FlaskForm):
    # 用户名输入框，变量名为name
    account = StringField(
        label='账号',
        validators=[
             DataRequired("请输入账号！")
        ],
        description="账号",
        # 可以设置一些style
        render_kw={
            'class': "form-control",
            'placeholder': "请输入账号！",
            #'required': 'required'  # 输入框如果为空则点登录时会提示
        }
    )
    # 密码输入框
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码！",
            #'required': 'required'
        }
    )
    # 提交按钮
    submit = SubmitField(
        '登录',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat"
        }
    )
    # 当点击登录时，该方法会被自动调用，用来判断用户名是否存在，并将结果显示到前端
    def validate_account(self, field):  # validate + 字段名
            account = field.data  # 获取到用户名输入
            admin = Admin.query.filter_by(name=account).count()  # 数据库查询
            if admin == 0:
                raise ValidationError("账号不存在")  # 显示到前端
```

3.在视图模块中进行表单验证：

``` python
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm  # 引入在form.py定义的表单
from app.models import Admin  # 引入数据库模型

@admin.route("/login/", methods=['GET', 'POST'])  # POST传入参数，需定义methods
def login():
    form = LoginForm()
    if form.validate_on_submit():  # 表单是否被提交
        data = form.data  # 字段名字和值组成的字典
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):  # 验证密码
            flash("密码错误！")  # 消息闪现
            return redirect(url_for('admin.login'))  # 失败则跳转到登录页面
        session['admin'] = data['account']  # 成功则创建session
        return redirect(request.args.get('next') or url_for('admin.index'))  # 并跳转到后台主页
    return render_template('admin/login.html', form=form)
```

需要在Admin模型中定义一个验证方法：

``` python
def check_pwd(self, pwd):
    from werkzeug.security import check_password_hash  # 验证hash密码
    return check_password_hash(self.pwd, pwd)  # 第一个参数为模型中的pwd，第二个为传入的pwd
```

4.在模板文件 app/template/admin/login.html 中定义表单，部分如下：

    <div class="login-box-body">
            {% for msg in get_flashed_messages() %} {# 用于消息闪现 #}
            <p class="login-box-msg" style="color:red">{{ msg }}</p>
            {% endfor %}
            <form method="POST" id="form-data">
                <div class="form-group has-feedback">
                    {{ form.account }} {# 传入views.py中创建的表单变量，便会在前端自动生成表单 #}
                    <span class="glyphicon glyphicon-envelope form-control-feedback"></span>
                    {% for err in form.account.errors %}  {# 捕获并显示错误，比如用户名不存在 #}
                    <div class="col-md-12">
                        <font style="color:red">{{ err }}</font>
                    </div>
                    {% endfor %}
                </div>
                <div class="form-group has-feedback">
                    {{ form.pwd }}
                    <span class="glyphicon glyphicon-lock form-control-feedback"></span>
                    {% for err in form.pwd.errors %}
                    <div class="col-md-12">
                        <font style="color:red">{{ err }}</font>
                    </div>
                    {% endfor %}
                    </div>
                <div class="row">
                    <div class="col-xs-8">
                    </div>
                    <div class="col-xs-4">
                        {{ form.submit }}
                        {{ form.csrf_token }}  {# 生成csrf #}
                    </div>
                </div>
            </form>
        </div>

闪现系统的基本工作方式是：在且只在下一个请求中访问上一个请求结束时记录的消息

#### 登出功能
在登出功能中实现销毁session：

``` python
# 登出
@admin.route("/logout/")
def logout():
    session.pop('admin', None)  # 销毁session
    return redirect(url_for('admin.login'))
```

但是这样还不能有效的验证，即使现在不登录，输入后台路径的话还是能访问的到的

#### 访问控制
继续上面的，当用户点击登出清空session后，此时访问后台路径，发现还是能够正常访问的，因为没有定义访问控制，应该在调用路由函数前进行判断是否存在用户正常的登录后的session，这就用到了装饰器

Flask中每一个视图都是一个装饰器，例如route()。我们可以定义一个自定义的装饰器。装饰器是一个返回函数的函数

``` python
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:  # 判断session
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
```

装饰器用于更新函数的 `__name__`、 `__module__` 和其他属性，但是不必人工更新函数属性，可以使用一个类似于装饰器的函数  functools.wraps() 

定义好装饰器后，要记住：要把定义的装饰器放在最靠近函数的地方！不然不会生效

例如：

``` python
@admin.route("/")
@admin_login_req
def index():
    return render_template('admin/index.html')
```

因为后台有很多视图，因此要在相应的地方添加此装饰器










