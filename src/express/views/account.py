# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from flask import (request, views, flash, redirect, 
				   url_for, render_template, current_app as app)
from express.blueprints import blueprint_www
from express.models.account import AccountModel, EmailModel


class SignUpView(views.MethodView):
    '''
        注册
    '''

    def post(self):
        return 'ok'


class LoginView(views.MethodView):
    '''
        登录
    '''

    def post(self):
    	flash("login failure!")
    	return redirect(url_for("views.index"))


class LogoutView(views.MethodView):
    '''
        退出
    '''

    def get(self):
        return 'ok'


blueprint_www.add_url_rule('/signup', view_func=SignUpView.as_view(b'signup'),
                                endpoint='signup', methods=['POST'])
blueprint_www.add_url_rule('/login', view_func=LoginView.as_view(b'login'),
                                endpoint='login', methods=['POST'])
blueprint_www.add_url_rule('/logout', view_func=LogoutView.as_view(b'logout'),
                                endpoint='logout', methods=['POST'])
