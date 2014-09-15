#! -*- coding: utf-8 -*-

from __future__ import unicode_literals


from flask import current_app as app
from studio.core.engines import db
from studio.core.contribs import feistel, base62


__all__ = [
    'AddressModel',
    'LogisticsModel',
    'BillModel',
    'ItemModel',
]


SerialIdSeq = db.Sequence('serial_id_seq')


def serial_id_nextval():
    # with db.disable_slaves():
    return db.session.execute(SerialIdSeq)


def serial_key_generator():
    orig_id = serial_id_nextval()
    fei = feistel.Feistel(
        app.config['FEISTEL_PRIVATE_KEY'], bits=128)
    return base62.base62_encode(fei.encrypt(orig_id))


class AddressModel(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    account_uid = db.Column(db.CHAR(32),
                            db.ForeignKey('account.uid'),
                            nullable=False)
    real_name = db.Column(db.Unicode(64), nullable=False, index=True)
    mobile = db.Column(db.Unicode(32), nullable=False)
    code = db.Column(db.Unicode(32), nullable=False)
    IDnumber = db.Column(db.Unicode(64), nullable=True)
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
    bill_id = db.Column(db.Integer(), db.ForeignKey('bill.id'), nullable=False)
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

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    account_uid = db.Column(db.CHAR(32),
                            db.ForeignKey('account.uid'),
                            nullable=False)
    genre = db.Column(db.Unicode(64), nullable=False, index=True)
    serial_num = db.Column(db.CHAR(32), default=serial_key_generator,
                           nullable=False, unique=True)
    address_id = db.Column(db.Integer(), db.ForeignKey('address.id'),
                           nullable=False)
    remark = db.Column(db.UnicodeText(), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    address = db.relationship('AddressModel',
                backref=db.backref('bills', lazy='joined'),
                primaryjoin='AddressModel.id==BillModel.address_id',
                uselist=False)

    logistics = db.relationship('LogisticsModel',
                backref=db.backref('bill', lazy='joined', innerjoin=True),
                primaryjoin='BillModel.id==LogisticsModel.bill_id',
                foreign_keys='[LogisticsModel.bill_id]')

    items = db.relationship('ItemModel',
                backref=db.backref('bill', lazy='joined', innerjoin=True),
                primaryjoin='BillModel.id==ItemModel.bill_id',
                foreign_keys='[ItemModel.bill_id]')

    def as_dict(self):
        return {
            'id': self.id,
            'serial_num': self.serial_num,
            'genre': self.genre,
            'remark': self.remark,
            'address': self.address.as_dict(),
            'date_created': self.date_created.isoformat(),
        }

    def __str__(self):
        return self.serial_num


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    bill_id = db.Column(db.Integer(), db.ForeignKey('bill.id'), nullable=False)
    name = db.Column(db.Unicode(256), nullable=False)
    genre = db.Column(db.Unicode(64), nullable=False, index=True)
    dollar = db.Column(db.Integer(), nullable=True)
    quantity = db.Column(db.Integer(), server_default=u'1', nullable=False)
    remark = db.Column(db.UnicodeText(), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

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
