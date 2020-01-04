# coding:utf8
# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import User
from flask import session


class RegisterForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired("请输入用户名！")
        ],
        description='用户名',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入用户名称！"
        }
    )

    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码！"
        }
    )

    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired("请输入重复密码！"),
            EqualTo('pwd', message='两次密码输入不一致！')
        ],
        description='确认密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请再次输入密码！"
        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确！")
        ],
        description='邮箱',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入用户邮箱！"
        }
    )

    phone = StringField(
        label='手机',
        validators=[
            DataRequired("请输入手机号码！"),
            Regexp("1[3458]\\d[9]", message="手机格式不正确！")
        ],
        description='手机号码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入手机号码！"
        }
    )

    submit = SubmitField(
        '确定',
        render_kw={
            'class': "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("用户名已被占用！")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已被占用！")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("用户名已被占用！")


class LoginForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired("请输入用户名！")
        ],
        description='用户名',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入用户名称！"
        }
    )

    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码！"
        }
    )

    submit = SubmitField(
        '确定',
        render_kw={
            'class': "btn btn-lg btn-primary btn-block"
        }
    )










