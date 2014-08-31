# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from studio.core.engines import db
from express.models.bill import (AddressModel, LogisticsModel,
                                 BillModel, ItemModel)
from express.panel.base import BaseView


class Address(BaseView):
    perm = 'bill'

    column_list = ['id', 'real_name', 'mobile',
                   'code', 'IDnumber', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Address, self).__init__(AddressModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Address, self).create_form(obj=obj)
        delattr(form, 'date_created')
        delattr(form, 'bills')
        return form

    def edit_form(self, obj=None):
        form = super(Address, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        delattr(form, 'bills')
        return form


class Logistics(BaseView):
    perm = 'bill'

    column_list = ['id', 'genre', 'infomation', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Logistics, self).__init__(LogisticsModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Logistics, self).create_form(obj=obj)
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Logistics, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form


class Bill(BaseView):
    perm = 'bill'

    column_list = ['id', 'order_num', 'remark', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Bill, self).__init__(BillModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Bill, self).create_form(obj=obj)
        delattr(form, 'date_created')
        delattr(form, 'order_num')
        delattr(form, 'items')
        return form

    def edit_form(self, obj=None):
        form = super(Bill, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        delattr(form, 'order_num')
        delattr(form, 'items')
        return form


class Item(BaseView):
    perm = 'bill'

    column_list = ['id', 'name', 'genre', 'dollar',
                   'quantity', 'remark', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Item, self).__init__(ItemModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Item, self).create_form(obj=obj)
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Item, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form
