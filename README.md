# FlaskProject-giligili

giligili干杯~(￣▽￣)~*

[demo](http://62.234.60.226:2020/1/)

此项目为使用HTML5+Bootstrap+Flask+MySQL5.7+python3.6搭建的一个视频播放网站

点击[这里](base.md)查看基础知识文档

点击[这里](build.md)查看搭建过程文档

-----------------------

### 将本地项目部署到服务器上

1.拷贝文件到服务器：

	scp -r flask_project root@xx.xx.xx.xx:/root/

2.mysql导出数据库数据：

	mysqldump -h localhost -u root -p xxx > xxx.sql

3.在服务器上导入数据：

	create database project;
	use project;
	source xxx.sql

4.查看本地安装的pip包，复制到一个文件中：

	pip freeze

在服务器上安装这些pip包：

	python3 -m pip install -r requirement.txt

5.更改 `app/__init__.py`中的数据库配置

6.切换到 manager.py 目录，执行命令：

	 python3 manage.py runserver

---------------------

### 注意事项

1.当删除预告时，再添加预告，由于MySQL的特性，此时该预告表(preview)的id为删除之后的id+1，由于模板文件是根据数据表id来展示的，此时会显示错误，要正常显示需要更改表的id为从1开始递增。修改id步骤：

    SET @i=0;
    UPDATE `tablename` SET `id`=(@i:=@i+1);

----------------

### 数据库使用配置
1.要将 app/models.py中下面这行注释掉：

	from app import db

之后去掉数据库配置的注释，并进行修改，使其能够连接到本地数据库：

``` python
# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# import pymysql, os
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@127.0.0.1:3306/project3"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = 'gtfly'
# app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')  # 设置上传文件保存路径
# app.debug = True
#
# db = SQLAlchemy(app)
```

之后去掉下面这一行注释：

	db.create_all()

2.注释掉

	db.create_all()

，因为已经创建过表了，接着去掉下面的注释来创建 role ：

``` python
# role = Role(
#     name='超级管理员',
#     auths=''
# )
# db.session.add(role)
# db.session.commit()
```

因为如果要创建管理员，需要选择管理员所属角色，因此先创建role，再创建admin；接着注释掉上面的语句，去掉注释：

``` python
# from werkzeug.security import generate_password_hash
#
# admin = Admin(
#     name="admin",
#     pwd=generate_password_hash("123456"),
#     is_super=0,
#     role_id=1
# )
#
# db.session.add(admin)
# db.session.commit()
```

其中，name为管理员账号，pwd为管理员密码，修改后运行便可成功创建管理员账号

创建完后记得把上面的恢复原样
















