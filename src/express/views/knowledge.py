# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import views, flash, redirect, url_for, render_template
from jinja2 import TemplateNotFound
from express.blueprints import blueprint_www


class KnowledgeListView(views.MethodView):
    '''
        文章列表页
    '''

    def get(self):
        return render_template('www/knowledge/list.html')


blueprint_www.add_url_rule('/knowledge',
                            view_func=KnowledgeListView.as_view(b'knowledge'),
                            endpoint='knowledge', methods=['GET'])


class KnowledgeDetailView(views.MethodView):
    '''
        文章页
    '''

    def get(self, name=None):
        if not name:
            return redirect(url_for('views.knowledge'))
        try:
            tpl = render_template('www/knowledge/%s.html' % name)
        except TemplateNotFound, e:
            flash('没能找到您要的文章！')
            return redirect(url_for('views.knowledge'))

        return tpl


blueprint_www.add_url_rule('/knowledge/<string:name>/',
                    view_func=KnowledgeDetailView.as_view(b'knowledge_detail'),
                    endpoint='knowledge_detail', methods=['GET'])
