# -*- code: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babelex import Babel
from studio.core.flask.app import StudioFlask
from studio.core.engines import db


app = StudioFlask(__name__)

db.init_app(app)
Babel(app=app, default_locale='zh')


with app.app_context():
    from microsite.panel import admin
    app.add_url_rule('/apps/%s/<path:filename>' %
                        app.name, endpoint='static', #subdomain='static',
                        view_func=app.send_static_file)