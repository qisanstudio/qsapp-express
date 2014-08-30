# -*- code: utf-8 -*-
from __future__ import unicode_literals

from .account import *  # noqa pyflakes:ignore
from .bill import *  # noqa pyflakes:ignore

from studio.core.engines import db
db.configure_mappers()
