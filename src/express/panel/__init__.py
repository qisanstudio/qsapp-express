# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .account import Role, Privilege, Account, Email
from .bill import Address, Logistics, Bill, Item

from flask.ext.admin import Admin


admin = Admin(name='起点速递后台', url='/admin')

# 账户管理
admin.add_view(Role(name='角色',
                         category='账户管理', endpoint='role'))
admin.add_view(Privilege(name='角色权限',
                         category='账户管理', endpoint='privilege'))
admin.add_view(Account(name='账户',
                         category='账户管理', endpoint='account'))
admin.add_view(Email(name='邮箱',
                         category='账户管理', endpoint='email'))

# 货单管理
admin.add_view(Address(name='地址',
                         category='货单管理', endpoint='address'))
#admin.add_view(Logistics(name='物流',
#                         category='货单管理', endpoint='logistics'))
admin.add_view(Bill(name='订单',
                         category='货单管理', endpoint='bill'))
#admin.add_view(Item(name='货物',
#                         category='货单管理', endpoint='item'))
