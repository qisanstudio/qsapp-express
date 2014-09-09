#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.admin.form import Select2Field

from wtforms import Form
from wtforms.fields import (StringField, IntegerField,
                            HiddenField, TextAreaField)


ITEM_GENRES = ['a', 'b', 'c', 'd']


class ItemForm(Form):
    id = HiddenField('id')
    name = StringField('name')
    genre = Select2Field('genre', choices=zip(ITEM_GENRES, ITEM_GENRES))
    dollar = IntegerField('dollar')
    quantity = IntegerField('quantity')
    remark = TextAreaField('remark')
