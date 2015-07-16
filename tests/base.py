#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-flask-sessions.
# https://github.com/pnegahdar/django-flask-sessions

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Parham Negahdar <pnegahdar@gmail.com>

from unittest import TestCase as PythonTestCase
import flask

from centralsession.flask_session import CentralSessionInterface

class TestCase(PythonTestCase):
    REDIS_URI = 'redis://127.0.0.1:6379/1'

    def get_flask_app(self):
        app = flask.Flask(__name__)
        app.session_interface = CentralSessionInterface(self.REDIS_URI)
        return app

