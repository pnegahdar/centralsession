from __future__ import unicode_literals

from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings

from python.session import SessionBackend


def get_backend():
    redis_uri = settings['CENTRAL_SESSION_REDIS_URI']
    return SessionBackend(redis_uri)


backend = get_backend()


class SessionStore(SessionBase):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def _get_or_create_session_key(self):
        if self._session_key is None:
            self._session_key = self._get_new_session_key()

        return self._session_key

    def load(self):
        try:
            return backend.get_session(self.session_key)
        except LookupError:
            self.create()
            return {}

    def exists(self, session_key):
        return backend.exists(session_key)

    def create(self):
        self.save(must_create=True)
        self.modified = True
        self._session_cache = {}

    def save(self, must_create=False):
        session_key = self._get_or_create_session_key()

        expire_in = self.get_expiry_age()

        data = self._get_session(no_load=must_create)

        backend.save(session_key, data, expire_in)

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
        backend.delete_session(session_key)
