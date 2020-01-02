# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag

tags = Tag.query.all()


class LoginForm(FlaskForm):
    # 管理员登录表单
    account = StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            'class': "form-control",
            'placeholder': "请输入账号！",
            # 'required': 'required'  # 输入框如果为空则点登录时会提示
        }
    )

    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码！",
            # 'required': 'required'
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):  # validate + 字段名
        account = field.data  # 获取到用户名输入
        admin = Admin.query.filter_by(name=account).count()  # 数据库查询
        if admin == 0:
            raise ValidationError("账号不存在")  # 显示到前端


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired("请输入标签！")
        ],
        description='标签',
        render_kw={
            'class': "form-control",
            'id': "input_name",
            'placeholder': "请输入标签名称！"
        }
    )

    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class MovieForm(FlaskForm):
    # 电影片名
    title = StringField(
        label='片名',
        validators=[
            DataRequired("请输入片名！")
        ],
        description='片名',
        render_kw={
            'class': "form-control",
            'id': "input_title",
            'placeholder': "请输入片名！"
        }
    )

    # 电影文件
    url = FileField(
        label='文件',
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件"
    )

    # 电影简介
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired("请输入简介！")
        ],
        description='简介',
        render_kw={
            'class': "form-control",
            'rows': "10",
        }
    )

    # 电影封面
    logo = FileField(
        label='封面',
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面"
    )

    # 电影星级
    star = SelectField(
        label='星级',
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            'class': "form-control",
        }
    )

    # 电影标签
    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],  # 列表生成器生成标签选项
        description="标签",
        render_kw={
            'class': "form-control",
        }
    )

    # 上映地区
    area = StringField(
        label='地区',
        validators=[
            DataRequired("请输入地区！")
        ],
        description='地区',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入地区！"
        }
    )

    # 片长
    length = StringField(
        label='片长',
        validators=[
            DataRequired("请输入片长！")
        ],
        description='片长',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入片长！"
        }
    )

    # 上映时间
    release_time = StringField(
        label='上映时间',
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description='上映时间',
        render_kw={
            'class': "form-control",
            'placeholder': "请选择上映时间！",
            'id': 'input_release_time'
        }
    )

    submit = SubmitField(
        '添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )
