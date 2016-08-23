import unittest
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.dj_settings")
settings._setup()
django.setup()

from tests.djmirror.session_test import SessionTestsMixin
import flask

from centralsession.django_session import SessionStore
from tests.base import TestCase


class DjangoSessionsTests(SessionTestsMixin, TestCase):
    backend = SessionStore

    @unittest.expectedFailure
    def test_actual_expiry(self):
        # The cookie backend doesn't handle non-default expiry dates, see #19201
        super(DjangoSessionsTests, self).test_actual_expiry()

    def test_interop(self):
        flask_app = self.get_flask_app()
        flask_app.config['debug'] = True
        check_key = 'session_key'
        self.assertEqual(self.session.get(check_key), None)
        self.session['foo'] = 'bar'
        self.session.save()

        @flask_app.route('/')
        def home():
            lookup_key = flask.request.args.get('q')
            value = flask.session.get(lookup_key)
            flask.session['here'] = 'yes'
            return str(value)

        resp = flask_app.test_client().get('/?q=foo&sessionid={}'.format(self.session.session_key))
        self.assertEqual(resp.data, 'bar')
        session = self.backend(self.session.session_key)
        self.assertEqual(session['here'], 'yes')
