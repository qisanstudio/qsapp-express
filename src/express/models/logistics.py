#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import url_for
from jinja2 import Markup
from sqlalchemy import sql
from studio.core.engines import db
from sqlalchemy.ext.hybrid import hybrid_property


__all__ = [
    'ArticleModel',
    'ArticleContentModel',
]


class ArticleModel(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    cid = db.Column('channel_id', db.Integer(), nullable=False, index=True)
    is_sticky = db.Column(db.Boolean(), nullable=False, server_default=sql.false())
    title = db.Column(db.Unicode(64), nullable=False, unique=True, index=True)

    date_published = db.Column(db.DateTime(timezone=True),
                            nullable=False, index=True,
                             server_default=db.func.current_timestamp())
    date_created = db.Column(db.DateTime(timezone=True),
                            nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    _content = db.relationship(
            'ArticleContentModel',
            backref=db.backref('article', lazy='joined', innerjoin=True),
            primaryjoin='ArticleModel.id==ArticleContentModel.id',
            foreign_keys='[ArticleContentModel.id]',
            uselist=False, cascade='all, delete-orphan')

    @property
    def url(self):
        return url_for('views.article', aid=self.id)

    @hybrid_property
    def content(self):
        return self._content.content

    @content.setter
    def content_setter(self, value):
        if not self._content:
            self._content = ArticleContentModel(id=self.id, content=value)
        self._content.content = value

    @property
    def html(self):
        return Markup(self.content)

    def __str__(self):
        return self.title


class ArticleContentModel(db.Model):
    __tablename__ = 'article_content'

    id = db.Column(db.Integer(), db.ForeignKey('article.id'),
                        nullable=False, primary_key=True)
    content = db.Column(db.UnicodeText(), nullable=False)
