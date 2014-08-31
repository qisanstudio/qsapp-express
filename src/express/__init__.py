# -*- code: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babelex import Babel
from studio.core.flask.app import StudioFlask
from studio.core.engines import db


app = StudioFlask(__name__)

db.init_app(app)
Babel(app=app, default_locale='zh')


with app.app_context():
    from express import views
    from express.panel import admin
    from express.blueprints import blueprint_www
    admin.init_app(app)

    assert views

    app.register_blueprint(blueprint_www)

    app.add_url_rule('/apps/%s/<path:filename>' %
                        app.name, endpoint='static', #subdomain='static',
                        view_func=app.send_static_file)


    if __name__ == '__main__':
        app.run(host='0.0.0.0')
