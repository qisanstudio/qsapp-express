# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask_wtf import Form
from wtforms import fields
from wtforms import validators
from express.models import EmailModel


class EmailMixin(object):
    email = fields.StringField(
        '邮箱',
        default='',
        description='请填写真实邮箱',
        validators=[
            validators.Required(message='邮箱是必填项'),
            validators.Email(message='邮箱格式不正确，请重新填写')
        ])


class LogInForm(EmailMixin, Form):
    password = fields.PasswordField(
        '密码', default='',
        validators=[validators.Required()])
    permanent = fields.BooleanField('记住我（网吧或别人的电脑请不要勾选）', default=True)



class SignUpForm(EmailMixin, Form):

    def validate_email(form, field):
        email = field.data
        count = EmailModel.query.filter_by(email_insensitive=email).count()
        if count:
            raise ValidationError('邮箱已被注册，是否需要登录？')