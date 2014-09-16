# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint_www = Blueprint('views', __name__)
blueprint_apis = Blueprint('apis', __name__, url_prefix='/apis')