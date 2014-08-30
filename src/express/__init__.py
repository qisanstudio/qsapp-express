# -*- code: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babelex import Babel
from studio.core.flask.app import StudioFlask
from studio.core.engines import db


app = StudioFlask(__name__)

app.secret_key = '\x94\xabM\x8c\xc8\r_x#\x06\x8ac\x99\xf5/\x83\xe7\xce\x04\x80XVs\xbe'
db.init_app(app)
Babel(app=app, default_locale='zh')


with app.app_context():
    from express import views
    from microsite.panel import admin
    from microsite.blueprints import blueprint_www
    admin.init_app(app)

    assert views

    app.register_blueprint(blueprint_www)

    app.add_url_rule('/apps/%s/<path:filename>' %
                        app.name, endpoint='static', #subdomain='static',
                        view_func=app.send_static_file)
