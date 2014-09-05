# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from flask import views, url_for, redirect, render_template, request, flash
from studio.core.engines import db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
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
		return 'ok'


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
		email = form.email.data
		password = form.password.data
		permanent = form.permanent.data
		email_obj = _get_email_obj(email)

		# 校验密码
		if email_obj:
			password_hash, _ = EmailModel.encrypt_password(
										password, email_obj.password_salt)
			if email.password_hash != password_hash:
				raise
			email.date_last_signed_in = datetime.now()
			db.session.commit()
#       session['sign_in_account'] = email.account.uid
		return redirect(url_for('views.home'))


class SignoutView(views.MethodView):
	'''
		退出
	'''

	def get(self):
		return 'ok'


blueprint_www.add_url_rule('/home',
							view_func=HomeView.as_view(b'home'),
							endpoint='home', methods=['GET'])
blueprint_www.add_url_rule('/signup',
							view_func=SignUpView.as_view(b'signup'),
							endpoint='signup', methods=['GET', 'POST'])
blueprint_www.add_url_rule('/signin',
							view_func=SignInView.as_view(b'signin'),
							endpoint='signin', methods=['GET', 'POST'])
blueprint_www.add_url_rule('/signout',
							view_func=SignoutView.as_view(b'signout'),
							endpoint='signout', methods=['POST'])
