# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .account import Role, RolePrivilege, Account, Email
from .bill import Address, Logistics, Bill, Item

from flask.ext.admin import Admin


pregnancy_admin = Admin(name='起点快运后台', url='/admin')

# 账户管理
pregnancy_admin.add_view(Role(name='角色',
                         category='账户管理', endpoint='role'))
pregnancy_admin.add_view(RolePrivilege(name='角色权限',
                         category='账户管理', endpoint='privilege'))
pregnancy_admin.add_view(Account(name='账户',
                         category='账户管理', endpoint='account'))
pregnancy_admin.add_view(Email(name='邮箱',
                         category='账户管理', endpoint='email'))

# 货单管理
pregnancy_admin.add_view(Address(name='地址',
                         category='货单管理', endpoint='address'))
pregnancy_admin.add_view(Logistics(name='物流',
                         category='货单管理', endpoint='logistics'))
pregnancy_admin.add_view(Bill(name='订单',
                         category='货单管理', endpoint='bill'))
pregnancy_admin.add_view(Item(name='货物',
                         category='货单管理', endpoint='item'))
