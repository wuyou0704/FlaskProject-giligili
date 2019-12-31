本篇主要记录相关的基础知识

目录

- [python包中的`__init__.py`](#python包中的`__init__.py`)
  - [功能](#功能)
  - [示例](#示例)
- [蓝图构建项目](#蓝图构建项目)
  - [什么是蓝图](#什么是蓝图)
  - [示例](#示例)
- [Flask-SQLAlchemy](#Flask-SQLAlchemy)
  - [SQLAlchemy中常用的配置键和值](#SQLAlchemy中常用的配置键和值]
  - [Column属性](#Column属性)
  - [连接数据库并创建表](#连接数据库并创建表)
  - [数据表的关系](#数据表的关系)
    - [一对多](#一对多)
    - [一对一](#一对一)
  - [数据安全性](#数据安全性)
- [template模板文件](#template模板文件)
  - [模板文件语法](#模板文件语法)
- [flask视图相关功能](#flask视图相关功能)

### python包中的`__init__.py`
#### 功能

在pycharm新建package时，默认会附带一个`__init__.py`空文件；其作用为：

1. 只要存在`__init__.py`，解释器就会把该目录当作一个package处理            
2. `__init__.py`文件的主要作用是导入该包内的其他模块


#### 示例
现有文件：

    ├── app
    │   ├── __init__.py
    │   └── say.py
    └── hello.py

首先在`app/say.py`定义了两个函数：

``` python
def say1():
	print('I am say1')

def say2():
	print('I am say2')
```

之后在`app/__init__.py`定义：

``` python
from .say import say1, say2
```

其中，`.`代表当前的包

那么便可在hellp.py中这样调用这两个函数：

``` python
from app import say1, say2

say1()
say2()
```

或者

``` python
from app import *

say1()
say2()
```

有木有很方便～

如果没有这个`__init__.py`，只能这样引入：

``` python
from app.say import *
from app.say import say1,say2
```

如果`app`这个包中除了`say`外，有很多其他的模块，那么要引入的话就会很麻烦，这时候`__init__.py`的作用就体现出来了


### 蓝图构建项目
#### 什么是蓝图
是一个存储视图方法的容器，这些操作在Blueprint被注册到一个应用之后就可以调用，Flask可以通过Blueprint来组织URL以及处理请求

蓝图的作用：

- 将不同的功能模块化
- 构建大型应用
- 优化项目结构
- 增强可读性，易于维护

#### 示例

1.创建一个蓝图对象`app/admin/__init__.py`：

``` python
from flask import Blueprint

admin = Blueprint("admin", __name__)

import app.admin.views
```

2.注册路由(创建视图)`app/admin/views.py`：

``` python
from . import admin

@admin.route("/")
def index():
	return "hello admin"
```

3.在应用对象上注册这个蓝图`app/__init__.py`：

``` python
from flask import Flask

app = Flask(__name__)

from app.admin import admin as admin_blueprint 
app.register_blueprint(admin_blueprint, url_prefix="/admin") 
# url_prefix为url添加前缀，此前缀会拼接到route的路径：此时url为`/admin/`时可访问路由，即`/admin` `/admin/`均可访问(唯一重定向)
```

4.定义程序入口`manage.py`(与app同一级)：

``` python
from app import app

if __name__ == '__main__':
	app.run()
```

### Flask-SQLAlchemy
#### SQLAlchemy中常用的配置键和值

1.`SQLALCHEMY_DATABASE_URI`：用于连接数据库；连接URI格式：

	dialect+driver://username:password@host:port/database

例如MYSQL：

	mysql://root:123456@localhost/mydatabase

SQLite (注意开头的四个斜线):

	sqlite:////absolute/path/to/foo.db

2.`SQLALCHEMY_TRACK_MODIFICATIONS`：如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。

#### Column属性
使用db.Column()来创建一个字段，参数类型大致如下：

字段类型(db.xxx)：

`Integer` ：一个整数   
`String (size)`：有长度限制的字符串   
`Text`：一些较长的 unicode 文本  
`DateTime`：表示为 Python datetime 对象的时间和日期   
`Float`：存储浮点值     
`Boolean`：存储布尔值   
`PickleType`：存储为一个持久化的 Python 对象    
`LargeBinary`：存储一个任意大的二进制数据

常用参数：

- primary_key：如果设为 True,这列就是表的主键       
- unique：如果设为 True,这列不允许出现重复的值       
- index：如果设为 True,为这列创建索引,提升查询效率      
- nullable：如果设为 True,这列允许使用空值;如果设为 False,这列不允许使用空值     
- default：为这列定义默认值        


#### 连接数据库并创建表

``` python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
# 连接test数据库;需安装pymysql包
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@127.0.0.1:3389/test" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# 会员表
class User(db.Model):
    # 定义表名
    __tablename__ = 'user'
    # 变量名即为字段名，db.xxx为字段类型，primary_key为标志的主键、unique为值的唯一性约束
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)

    def __repr__(self):
        return "<User %r>" % self.name

if __name__ == '__main__':
    # 创建所有表
    db.create_all()
```

相关解释：

- `__repr__()`：它是一个“自我描述”的方法，该方法通常用于实现这样一个功能：当程序员直接打印该对象时，系统将会输出该对象的“自我描述”信息，用来告诉外界该对象具有的状态信息。
- `%r`是个万能格式符

表操作：
db.create_all()：创建所有表   
db.session.add(me)：添加数据   
db.session.commit()：提交    

当往表中插入中文时，可能会报错；解决方法：可以在创建数据库时就设置数据库的字符编码：

	create database project default character set utf8;

#### 数据表的关系
##### 一对多
例如以下两个数据库模型：

``` python
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='person',
                                lazy='dynamic')

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
```

`db.relationship`默认用于在表中建立一对多关系；

在Person类中：

	addresses = db.relationship('Address', backref='person',lazy='dynamic')

relationship提供了Person对Address的访问；backref正好相反，提供了Address对person的访问

lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据:

- 'select' (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
- 'joined' 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
- 'subquery' 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
- 'dynamic' 在有多条数据的时候是特别有用的。不是直接加载这些数据，SQLAlchemy 会返回一个查询对象，在加载数据前您可以过滤（提取）它们。

##### 一对一
在`relationship()`中设置`uselist=False` 参数 

#### 数据安全性
数据库中直接存放明文密码是很危险的,werkzeug库中的security能够方便的实现散列密码的计算：

	from werkzeug.security import generate_password_hash

### template模板文件
Jinja2：是 Python 下一个被广泛应用的模板引擎，是由Python实现的模板语言；Flask是使用 Jinja2 这个模板引擎来渲染模板

Flask提供的 render_template 函数封装了该模板引擎；render_template 函数的第一个参数是模板的文件名，后面的参数都是键值对，表示模板中变量对应的真实值。

#### 模板文件语法
模板文件夹要命名为template；

1.url_for()：可实现页面跳转、加载静态资源

	<link rel="shortcut icon" href="{{ url_for('static', filename='base/images/logo.png') }}">

此时，logo.png要位于与template同级目录的 static/base/images/logo.png

2.表示变量名

``` python
{{ xxx }}
```

3.注释

使用 {# #} 进行注释，注释的内容不会在html中被渲染出来

4.定义控制代码块，可以实现一些语言层次的功能，比如循环或者if语句

``` python
{% if user %}
	{{ user }}
{% else %}
	hello!
<ul>
	{% for index in indexs %}
	<li> {{ index }} </li>
	{% endfor %}
</ul>
```

5.模板继承

目的：为了减少前端代码量

语法：

``` jinja2
{% extends "base.html" %}

{% block name %}
....
{% endblock %}
```

比如在home/home.html中添加：

``` html
<div class="container" style="margin-top:76px">
	{% block content %}{% endblock %}
</div>
```

那么同级目录的home/index.html来继承该模板，并设置自己独有的显示：

``` html
{% extends "home/home.html" %}

{% block content %}  # content要与home.html中设定的block名字相同
<h1>hello world</h1>
{% endblock %}
```

那么现在这两个模板页面唯一的区别是index.html中多了个 hello world

6.模板包含

	{% includes 'home/menu.html' %}

### flask视图相关功能

``` python
from flask import render_template, redirect, url_for

@home.route('/login/')
def login():
	# 返回模板
    return render_template('home/login.html')


@home.route('/logout/')
def logout():
    return redirect(url_for('home.login'))
```

redirect() 可以重定向，使用方法：

1.直接用，可以直接写完整链接，可以写视图函数路径

2.配合url_for一起用，url_for里面为函数名，如果注册了蓝图，则为蓝图名字.函数名

url_for() ：

1.url_for()是对函数进行操作

2.可以用来构造url，例如上面模板中加载静态资源


























