from datetime import timedelta

from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from centralsession.backend import SessionBackend

def get_backend(redis_uri, key_prefix=None):
    kwargs = {}
    if key_prefix:
        kwargs['key_prefix'] = key_prefix
    return SessionBackend(redis_uri, **kwargs)


class CentralSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class CentralSessionInterface(SessionInterface):
    session_class = CentralSession

    def __init__(self, redis_uri, key_prefix=None, sessionid_param='sessionid',
                 sessionid_header='sessionid'):
        self.redis_uri = redis_uri
        self.key_prefix = key_prefix
        self.session_request_key = sessionid_param
        self.session_header_field = sessionid_header

    @property
    def backend(self):
        return get_backend(self.redis_uri, self.key_prefix)


    def get_sessionid_from_request(self, request):
        return request.headers.get(self.session_header_field) or request.form.get(
            self.session_request_key) or request.args.get(self.session_request_key)

    def generate_sid(self):
        return self.backend._get_random_key(32)

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name) or self.get_sessionid_from_request(
            request)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.backend.get_session(sid)
        if val:
            return self.session_class(val, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.backend.delete_session(session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        self.backend.save(session.sid, dict(session), int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)

