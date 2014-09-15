#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.admin.form import Select2Field

from wtforms import Form
from wtforms.fields import (StringField, IntegerField,
                            HiddenField, TextAreaField)


ITEM_GENRES = [('clothing', '服饰'),
				('footwear', '鞋靴'),
				('sporting', '运动物品'),
				('care', '护理卫生用品'),
				('baby', '母婴用品'),
				('adult', '成人用品'),
				('commodity', '日用品'),
				('av', '音像制品'),
				('toy', '玩具'),
				('luggage', '箱包'),
				('books', '书籍'),
				('stationery', '文具'),
				('snacks', '零食'),
				('health', '保健品'),
				('cosmetics', '化妆品'),
				('jewelry', '首饰'),
				('digital', '数码产品'),
				('appliances', '电器类'),
				('musical', '乐器类'),
				('banner', '名牌包')]

LOGISTICS_GENRES = [('warehouse', '入库'), 
					('clearance', '清关'), 
					('ems', 'EMS')]


class ItemForm(Form):
    id = HiddenField('id')
    name = StringField('name')
    genre = Select2Field('genre', choices=ITEM_GENRES)
    dollar = IntegerField('dollar')
    quantity = IntegerField('quantity')
    remark = TextAreaField('remark')


class LogisticsForm(Form):
    id = HiddenField('id')
    genre = Select2Field('genre', choices=LOGISTICS_GENRES)
    infomation = TextAreaField('remark')
