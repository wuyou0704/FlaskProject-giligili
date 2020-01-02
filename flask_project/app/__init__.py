# coding='utf-8'
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql, os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@127.0.0.1:3306/project"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'gtfly'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')  # 设置上传文件保存路径
app.debug = True

db = SQLAlchemy(app)


from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 404错误处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
