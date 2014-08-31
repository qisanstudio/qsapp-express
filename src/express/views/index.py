# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from flask import request, views, render_template
from express.blueprints import blueprint_www


class IndexView(views.MethodView):
    '''
        首页
    '''

    def get(self):
        return render_template('www/index.html')


blueprint_www.add_url_rule('/', view_func=IndexView.as_view(b'index'),
                                endpoint='index', methods=['GET'])