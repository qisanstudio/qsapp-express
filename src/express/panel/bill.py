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


class Logistics(BaseView):
    perm = 'bill'

    column_list = ['id', 'genre', 'infomation', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Logistics, self).__init__(LogisticsModel, db.session, **kwargs)


class Bill(BaseView):
    perm = 'bill'

    column_list = ['uid', 'order_num', 'remark', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Bill, self).__init__(BillModel, db.session, **kwargs)


class Item(BaseView):
    perm = 'bill'

    column_list = ['id', 'name', 'genre', 'dollar',
                   'quantity', 'remark', 'date_created']
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Item, self).__init__(ItemModel, db.session, **kwargs)
