#! -*- coding: utf-8 -*-

from __future__ import unicode_literals


from studio.core.engines import db
from studio.core.flask.helpers import gen_uuid


__all__ = [
    'AddressModel',
    'LogisticsModel',
    'BillModel',
    'ItemModel',
]


class AddressModel(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    real_name = db.Column(db.Unicode(64), nullable=False, index=True)
    mobile = db.Column(db.Unicode(32), nullable=False)
    code = db.Column(db.Unicode(32), nullable=False)
    IDnumber = db.Column(db.Unicode(64), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'real_name': self.real_name,
            'mobile': self.mobile,
            'code': self.code,
            'IDnumber': self.IDnumber,
            'date_created': self.date_created.isoformat(),
        }

    def __str__(self):
        return '%s <%s>' % (self.real_name, self.mobile)


class LogisticsModel(db.Model):
    __tablename__ = 'logistics'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    genre = db.Column(db.Unicode(64), nullable=False, index=True)
    infomation = db.Column(db.UnicodeText(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    def as_dict(self):
        return {
            'genre': self.genre,
            'infomation': self.infomation,
            'date_created': self.date_created.isoformat(),
        }


class BillModel(db.Model):
    __tablename__ = 'bill'

    uid = db.Column(db.CHAR(32), nullable=False,
                    default=gen_uuid, primary_key=True)
    order_num = db.Column(db.Integer(), nullable=False, unique=True)
    address_id = db.Column(db.Integer(), db.ForeignKey('address.id'),
                           nullable=False)
    remark = db.Column(db.UnicodeText(), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    address = db.relationship('AddressModel',
                backref=db.backref('bills', lazy='joined', innerjoin=True),
                primaryjoin='AddressModel.id==BillModel.address_id',
                foreign_keys='[AddressModel.id]')

    def as_dict(self):
        return {
            'uid': self.uid,
            'order_num': self.order_num,
            'remark': self.remark,
            'address': self.address.as_dict(),
            'date_created': self.date_created.isoformat(),
        }

    def __str__(self):
        return self.order_num


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    bill_uid = db.Column(db.CHAR(32),
                         db.ForeignKey('bill.uid'), nullable=False)
    name = db.Column(db.Unicode(256), nullable=False)
    genre = db.Column(db.Unicode(64), nullable=False, index=True)
    dollar = db.Column(db.Integer(), nullable=True)
    quantity = db.Column(db.Integer(), server_default=u'1', nullable=False)
    remark = db.Column(db.UnicodeText(), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    bill = db.relationship('BillModel',
                backref=db.backref('items', lazy='joined', innerjoin=True),
                primaryjoin='BillModel.uid==ItemModel.bill_uid',
                foreign_keys='[BillModel.id]')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre,
            'dollar': self.dollar,
            'quantity': self.quantity,
            'remark': self.remark,
            'date_created': self.date_created.isoformat(),
        }

    def __str__(self):
        return self.name
