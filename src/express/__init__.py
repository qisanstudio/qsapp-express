# -*- code: utf-8 -*-
from __future__ import unicode_literals

from studio.core.flask.app import StudioFlask


app = StudioFlask(__name__)

with app.app_context():
    from express import views
    from express import apis
    from express.panel import admin
    from express.blueprints import blueprint_www, blueprint_apis
    admin.init_app(app)

    assert views
    assert apis

    app.register_blueprint(blueprint_www)
    app.register_blueprint(blueprint_apis)

    app.add_url_rule('/apps/%s/<path:filename>' %
                        app.name, endpoint='static', #subdomain='static',
                        view_func=app.send_static_file)
