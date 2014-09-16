# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request
from datetime import datetime

from flask.ext.admin.actions import action
from flask.ext.admin.contrib.sqla import ModelView


labels = dict(
        id='ID',
        date_created='创建时间',
    )


class BaseView(ModelView):

    column_labels = labels
    column_display_pk = True
    form_ajax_refs = None

    def is_accessible(self):
        return self.perm in request.current_user['privileges']

    @property
    def perm(self):
        return self.model.__tablename__

    @action('delete', '删除', '确定选中的删除吗')
    def action_delete(self, ids):
        model = self.model
        if hasattr(model, 'deleted'):
            self.session.flush()
            if ids:
                for m in model.query.filter(model.id.in_(ids)).all():
                    self.session.delete(m, reason='deleted_by_admin')
            self.session.commit()
        else:
            super(BaseView, self).action_delete(ids)

    @action('restore', '恢复', '确定要恢复已经删除的吗！')
    def action_restore(self, ids):
        model = self.model
        if model.__tablename__.endswith('deleted'):
            self.session.flush()
            if ids:
                for m in model.query.filter(model.id.in_(ids)).all():
                    m.restore()
            self.session.commit()

    def is_action_allowed(self, name):
        if name == 'restore':
            if hasattr(self, 'can_restore') and self.can_restore:
                return True
            return False
        return super(BaseView, self).is_action_allowed(name)

    def create_form(self, obj=None):
        form = super(BaseView, self).create_form(obj=obj)
        if hasattr(form, 'csrf_enabled'):
            form.csrf_enabled = False
        return form

    def edit_form(self, obj=None):
        form = super(BaseView, self).edit_form(obj=obj)
        if hasattr(form, 'csrf_enabled'):
            form.csrf_enabled = False
        return form

    def delete_model(self, model):
        self.session.delete(model, reason='deleted_by_admin')
        self.session.commit()

    def get_list_value(self, model, name):
        value = super(BaseView, self).get_list_value(self, model, name)
        try:
            if len(value) > 200:
                value = value[:200] + u'...'
        except:
            pass
        if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, int) and (value == -1):
            return '无记录'
        else:
            return value
