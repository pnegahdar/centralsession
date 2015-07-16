from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings

from centralsession.backend import SessionBackend

REDIS_URI_SETTING = 'CENTRAL_SESSION_REDIS_URI'
KEY_PREFIX_SETTING = 'CENTRAL_SESSION_KEY_PREFIX'


def get_backend():
    if not hasattr(settings, REDIS_URI_SETTING):
        raise ValueError('Setting {} must be set.'.format(REDIS_URI_SETTING))
    redis_uri = getattr(settings, REDIS_URI_SETTING)
    key_prefix = getattr(settings, KEY_PREFIX_SETTING, None)
    kwargs = {}
    if key_prefix:
        kwargs['key_prefix'] = key_prefix
    return SessionBackend(redis_uri, **kwargs)


backend = get_backend()


class SessionStore(SessionBase):
    def __init__(self, session_key=None):
        if session_key and not backend.exists(session_key):
            session_key = None
        super(SessionStore, self).__init__(session_key)

    def _get_or_create_session_key(self):
        if self._session_key is None:
            self._session_key = self._get_new_session_key()

        return self._session_key

    def load(self):
        try:
            if self.session_key:
                return backend.get_session(self.session_key)
        except LookupError:
            pass
        self.create()
        return {}

    def exists(self, session_key):
        return backend.exists(session_key)

    def create(self):
        self._session_cache = {}
        self.save(must_create=True)
        self.modified = True

    def save(self, must_create=False):
        session_key = self._get_or_create_session_key()
        expire_in = self.get_expiry_age()
        data = self._get_session(no_load=must_create)
        backend.save(session_key, data, expire_in)

    def delete(self, session_key=None):
        session_key = session_key or self.session_key
        if session_key is None:
            return
        backend.delete_session(self.session_key)
        self._session_key = None

    @classmethod
    def clear_expired(cls):
        pass
