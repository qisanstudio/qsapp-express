# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime
from flask import (views, url_for, redirect,
                    render_template, request, flash, session)
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from studio.core.engines import db, shared_redis
from express.blueprints import blueprint_www
from express.models.account import AccountModel, EmailModel

from . import forms


def _get_email_obj(address):
    try:
        email = EmailModel.query.filter_by(email=address).one()
    except NoResultFound:
        email = None
    except MultipleResultsFound:
        raise
    return email


class HomeView(views.MethodView):
    '''
        主页
    '''

    def get(self):
        return render_template('www/home.html')


class SignUpView(views.MethodView):
    '''
        注册
    '''

    def get(self):
        form = forms.SignUpForm()
        return render_template('www/signup.html', form=form)

    def post(self):
        form = forms.SignUpForm(request.form)
        if not form.validate():
            for _, es in form.errors.items():
                map(lambda e: flash(e), es)
            return redirect(url_for('views.signup'))
        nickname = form.nickname.data
        email = form.email.data
        password = form.password.data
        repeat_password = form.repeat_password.data
        email_obj = _get_email_obj(email)

        if email_obj:
            flash('Email had been used')
            return redirect(url_for('views.signup'))
        account = AccountModel(nickname=nickname)
        account.email = EmailModel(email=email,
                                    password=password)
        db.session.add(account)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            flash('Create account failed, reason is %s' % str(e))
            return redirect(url_for('views.signup'))

        session['sign_in_account'] = account.uid
        shared_redis.set('passport-access:%s' % session.sid,
                         json.dumps(account.as_dict()))
        resp = redirect(url_for('views.home'))
        resp.set_cookie('sid', session.sid, max_age=None)

        return resp


class SignInView(views.MethodView):
    """登录并准备session"""

    def get(self):
        form = forms.SignInForm()
        return render_template('www/signin.html', form=form)

    def post(self):
        form = forms.SignInForm(request.form)
        if not form.validate():
            flash('login error')
            return redirect(url_for('views.signin'))
        email = form.email.data.strip()
        password = form.password.data.strip()
        permanent = form.permanent.data
        email_obj = _get_email_obj(email)

        # 校验密码
        if not email_obj:
            flash('accout not exist')
            return redirect(url_for('views.signin'))

        password_hash, _ = EmailModel.encrypt_password(
                                    password, email_obj.password_salt)
        if email_obj.password != password_hash:
            flash('邮箱或密码错误，请重新登录！')
            return redirect(url_for('views.signin'))
        email_obj.date_last_signed_in = datetime.now()
        db.session.commit()

        session['sign_in_account'] = email_obj.account.uid
        shared_redis.set('passport-access:%s' % session.sid,
                         json.dumps(email_obj.account.as_dict()))
        resp = redirect(url_for('views.home'))
        resp.set_cookie('sid', session.sid, max_age=None)

        return resp


class SignoutView(views.View):
    '''
        退出
    '''

    def dispatch_request(self, uid):
        sess_uid = session.get('sign_in_account')
        resp = redirect(url_for('views.index'))
        if sess_uid != uid and sess_uid is not None:
            return resp  # 静默处理
        session.pop('sign_in_account', None)
        session.clear()

        resp.set_cookie('sid', max_age=0)
        return resp


blueprint_www.add_url_rule('/home',
                            view_func=HomeView.as_view(b'home'),
                            endpoint='home', methods=['GET'])
blueprint_www.add_url_rule('/signup',
                            view_func=SignUpView.as_view(b'signup'),
                            endpoint='signup', methods=['GET', 'POST'])
blueprint_www.add_url_rule('/signin',
                            view_func=SignInView.as_view(b'signin'),
                            endpoint='signin', methods=['GET', 'POST'])
blueprint_www.add_url_rule('/signout/<string:uid>/',
                            view_func=SignoutView.as_view(b'signout'),
                            endpoint='signout', methods=['GET'])
