import pickle
from datetime import datetime
import uuid

import flask

from tests.base import TestCase




class FlaskSessionTests(TestCase):


    def test_session(self):
        app = self.get_flask_app()
        app.secret_key = 'testkey'

        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @app.route('/get')
        def get():
            return flask.session['value']

        c = app.test_client()
        assert c.post('/set', data={'value': '42'}).data == b'value set'
        assert c.get('/get').data == b'42'


    def test_session_using_server_name(self):
        app = self.get_flask_app()
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='example.com'
        )

        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com/')
        assert 'domain=.example.com' in rv.headers['set-cookie'].lower()
        assert 'httponly' in rv.headers['set-cookie'].lower()
#

    def test_session_using_server_name_and_port(self):
        app = flask.Flask(__name__)
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='example.com:8080'
        )

        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com:8080/')
        assert 'domain=.example.com' in rv.headers['set-cookie'].lower()
        assert 'httponly' in rv.headers['set-cookie'].lower()


    def test_session_using_server_name_port_and_path(self):
        app = flask.Flask(__name__)
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='example.com:8080',
            APPLICATION_ROOT='/foo'
        )

        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com:8080/foo')
        assert 'domain=example.com' in rv.headers['set-cookie'].lower()
        assert 'path=/foo' in rv.headers['set-cookie'].lower()
        assert 'httponly' in rv.headers['set-cookie'].lower()


    def test_session_using_application_root(self):
        class PrefixPathMiddleware(object):

            def __init__(self, app, prefix):
                self.app = app
                self.prefix = prefix

            def __call__(self, environ, start_response):
                environ['SCRIPT_NAME'] = self.prefix
                return self.app(environ, start_response)

        app = flask.Flask(__name__)
        app.wsgi_app = PrefixPathMiddleware(app.wsgi_app, '/bar')
        app.config.update(
            SECRET_KEY='foo',
            APPLICATION_ROOT='/bar'
        )

        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://example.com:8080/')
        assert 'path=/bar' in rv.headers['set-cookie'].lower()


    def test_session_using_session_settings(self):
        app = flask.Flask(__name__)
        app.config.update(
            SECRET_KEY='foo',
            SERVER_NAME='www.example.com:8080',
            APPLICATION_ROOT='/test',
            SESSION_COOKIE_DOMAIN='.example.com',
            SESSION_COOKIE_HTTPONLY=False,
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_PATH='/'
        )

        @app.route('/')
        def index():
            flask.session['testing'] = 42
            return 'Hello World'
        rv = app.test_client().get('/', 'http://www.example.com:8080/test/')
        cookie = rv.headers['set-cookie'].lower()
        assert 'domain=.example.com' in cookie
        assert 'path=/' in cookie
        assert 'secure' in cookie
        assert 'httponly' not in cookie


    def test_missing_session(self):
        app = flask.Flask(__name__)

        def expect_exception(f, *args, **kwargs):
            try:
                f(*args, **kwargs)
            except RuntimeError as e:
                assert e.args and 'session is unavailable' in e.args[0]
            else:
                assert False, 'expected exception'
        with app.test_request_context():
            assert flask.session.get('missing_key') is None
            expect_exception(flask.session.__setitem__, 'foo', 42)
            expect_exception(flask.session.pop, 'foo')


    def test_session_stored_last(self):
        app = flask.Flask(__name__)
        app.secret_key = 'development-key'
        app.testing = True

        @app.after_request
        def modify_session(response):
            flask.session['foo'] = 42
            return response

        @app.route('/')
        def dump_session_contents():
            return repr(flask.session.get('foo'))

        c = app.test_client()
        assert c.get('/').data == b'None'
        assert c.get('/').data == b'42'


    def test_session_special_types(self):
        app = flask.Flask(__name__)
        app.secret_key = 'development-key'
        app.testing = True
        now = datetime.utcnow().replace(microsecond=0)
        the_uuid = uuid.uuid4()

        @app.after_request
        def modify_session(response):
            flask.session['m'] = flask.Markup('Hello!')
            flask.session['u'] = the_uuid
            flask.session['dt'] = now
            flask.session['b'] = b'\xff'
            flask.session['t'] = (1, 2, 3)
            return response

        @app.route('/')
        def dump_session_contents():
            return pickle.dumps(dict(flask.session))

        c = app.test_client()
        c.get('/')
        rv = pickle.loads(c.get('/').data)
        assert rv['m'] == flask.Markup('Hello!')
        assert type(rv['m']) == flask.Markup
        assert rv['dt'] == now
        assert rv['u'] == the_uuid
        assert rv['b'] == b'\xff'
        assert type(rv['b']) == bytes
        assert rv['t'] == (1, 2, 3)


