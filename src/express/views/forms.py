# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask_wtf import Form
from wtforms import fields, validators, ValidationError
from studio.core.wtf.validators import Nickname, CJKLength

from express.models import EmailModel


class EmailMixin(object):
    email = fields.StringField(
        '邮箱',
        default='',
        description='请填写真实邮箱',
        validators=[
            validators.Required(message='邮箱是必填项'),
            validators.Email(message='邮箱格式不正确，请重新填写'),
        ])


class SignInForm(EmailMixin, Form):
    password = fields.PasswordField(
        '密码', default='',
        validators=[validators.Required()])
    permanent = fields.BooleanField('记住我（网吧或别人的电脑请不要勾选）',
                                    default=True)


class SignUpForm(EmailMixin, Form):

    nickname = fields.StringField(
        '昵称', default='', validators=[
            validators.Required(message='昵称是必填项'), Nickname(),
            CJKLength(max=10)])
    password = fields.PasswordField('密码',
                                    validators=[validators.Required()])
    repeat_password = fields.PasswordField('重复密码',
                                           validators=[validators.Required()])

    def validate_email(form, field):
        email = field.data
        count = EmailModel.query.filter_by(email=email).count()
        if count:
            raise ValidationError('邮箱已被注册，请更换其它邮箱！')

    def validate_repeat_password(form, field):
        password = form.password.data
        repeat_password = field.data
        if password != repeat_password:
            raise ValidationError('两次密码不一致')
        if len(password) < 6:
            raise ValidationError('密码最少六位')


class BillSearchForm(EmailMixin, Form):
    serial_num = fields.TextAreaField(
        '订单号', validators=[validators.Required()])
