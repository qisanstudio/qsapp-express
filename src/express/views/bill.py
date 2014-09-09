# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import views, request, render_template
from express.blueprints import blueprint_www
from express.models.bill import BillModel

from . import forms


class BillSearchView(views.MethodView):
    '''
        订单搜索
    '''

    def get(self):
        form = forms.BillSearchForm()
        return render_template('www/bill/search.html', form=form)

    def post(self):
        form = forms.BillSearchForm(request.form)
        serial_num = form.serial_num.data
        bills = BillModel.query.filter_by(serial_num=serial_num).all()
        return render_template('www/bill/search.html', form=form, bills=bills)


blueprint_www.add_url_rule('/bill/search',
                           view_func=BillSearchView.as_view(b'bill_search'),
                           endpoint='bill_search', methods=['GET', 'POST'])
