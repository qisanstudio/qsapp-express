#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import base64
import hashlib
from hmac import HMAC
from flask.helpers import locked_cached_property
from sqlalchemy.ext.hybrid import hybrid_property

from studio.core.engines import db
from studio.core.flask.helpers import gen_uuid


__all__ = [
    'RoleModel',
    'RolePrivilegeModel',
    'AccountModel',
    'EmailModel',
]


_sha1 = lambda t: hashlib.sha1(t).hexdigest()
_base64_encode = lambda t: base64.b64encode(t)
_base64_decode = lambda t: base64.b64decode(t)


class RolePrivilegeModel(db.Model):
    __tablename__ = 'role_privilege'

    role_id = db.Column(db.CHAR(6), db.ForeignKey('role.id'),
                        primary_key=True, index=True)
    priv_id = db.Column(db.Integer(), db.ForeignKey('privilege.id'),
                        primary_key=True, index=True)


class RoleModel(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    title = db.Column(db.Unicode(64), nullable=False, unique=True)

    privileges = db.relationship('PrivilegeModel',
                                 secondary=RolePrivilegeModel.__table__)

    def as_dict(self):
        return {
            'title': self.title,
        }

    def __str__(self):
        return self.title


class PrivilegeModel(db.Model):
    __tablename__ = 'privilege'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    code = db.Column(db.CHAR(64), nullable=False, unique=True)
    description = db.Column(db.Unicode(64), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    def __str__(self):
        return self.description


class AccountModel(db.Model):
    __tablename__ = 'account'

    uid = db.Column(db.CHAR(32), nullable=False,
                                 default=gen_uuid,
                                 primary_key=True)
    nickname = db.Column(db.Unicode(256), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    email = db.relationship('EmailModel',
            backref=db.backref('account'),
            primaryjoin='AccountModel.uid==EmailModel.uid',
            uselist=False, passive_deletes=True)

    role = db.relationship('RoleModel',
                            backref=db.backref('accounts', lazy='joined'),
                            primaryjoin='AccountModel.role_id==RoleModel.id',
                            foreign_keys='[RoleModel.id]')

    addresses = db.relationship('AddressModel',
                                backref=db.backref('account', lazy='joined'),
                                primaryjoin='AddressModel.account_uid'
                                            '==AccountModel.uid',
                                foreign_keys='[AddressModel.account_uid]')

    bills = db.relationship('BillModel',
                            backref=db.backref('account', lazy='joined'),
                            primaryjoin='BillModel.account_uid'
                                        '==AccountModel.uid',
                            foreign_keys='[BillModel.account_uid]')

    @locked_cached_property
    def privileges(self):
        return [p.code for p in self.role.privileges]

    def as_dict(self):
        result = {
            'uid': self.uid,
            'nickname': self.nickname,
            'addresses': [address.as_dict() for address in self.addresses],
            'date_created': self.date_created,
        }
        if self.role:
            result['role'] = self.role.as_dict()
        return result

    def __str__(self):
        return self.nickname


class EmailModel(db.Model):
    __tablename__ = 'email'

    uid = db.Column(db.CHAR(32), db.ForeignKey('account.uid'),
                    primary_key=True, nullable=False)
    email = db.Column(db.String(256), nullable=False,
                      primary_key=True, index=True)
    password_hash = db.Column('password_hash', db.String(64), nullable=False)
    password_salt = db.Column('password_salt', db.String(64), nullable=False)
    date_last_signed_in = db.Column('date_last_signed_in',
                                    db.DateTime(timezone=True),
                                    server_default=db.func.current_timestamp(),
                                    index=True)
    date_created = db.Column('date_created',
                             db.DateTime(timezone=True),
                             server_default=db.func.current_timestamp(),
                             nullable=False,
                             index=True)

    @hybrid_property
    def password(self):
        return self.password_hash.strip()

    @password.setter
    def password_setter(self, value):
        self.password_hash, self.password_salt = self.encrypt_password(value)

    @staticmethod
    def encrypt_password(password, salt=None):
        """Hash password on the fly"""
        if salt is None:
            salt = os.urandom(8) # 64 bits
        if len(salt) != 8:
            salt = _base64_decode(salt)

        assert 8 == len(salt)
        assert isinstance(salt, str)

        if isinstance(password, unicode):
            password = password.encode('UTF-8')
        assert isinstance(password, str)

        result = password
        for i in xrange(10):
            result = HMAC(result, salt, hashlib.sha256).digest()

        return _base64_encode(result), _base64_encode(salt)

    @classmethod
    def is_email_avaliable(cls, email):
        query = cls.query.filter(db.func.lower(cls.email)==email.lower())
        return not query.count()

    def as_dict(self):
        return {
            'email': self.email,
            'date_last_signed_in': self.date_last_signed_in.isoformat(),
            'date_created': self.date_created.isoformat(),
        }

    def __str__(self):
        return self.email
