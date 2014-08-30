# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, url_for, flash, redirect
from flask.ext.admin import expose
from flask.ext.admin.babel import gettext
from flask.ext.admin.actions import action

from studio.core.engines import db

from express.models.account import (RoleModel, RolePrivilegeModel,
                                    AccountModel, EmailModel)
from express.panel.base import BaseView


class Role(BaseView):
    perm = 'role'

    column_list = ['id', 'title']
    column_default_sort = ('id', True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(RoleModel, db.session, **kwargs)


class Privilege(BaseView):
    perm = 'role'

    column_list = ['id', 'code', 'description', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Privilege, self).__init__(PrivilegeModel, db.session, **kwargs)


class Account(BaseView):
    perm = 'account'

    column_list = ['uid', 'nickname', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Account, self).__init__(AccountModel, db.session, **kwargs)


class Email(BaseView):
    perm = 'account'

    column_list = ['uid', 'email', 'date_last_signed_in', 'date_created']
    column_default_sort = ('date_last_signed_in', True)

    def __init__(self, **kwargs):
        super(Email, self).__init__(EmailModel, db.session, **kwargs)
