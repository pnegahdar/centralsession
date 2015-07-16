from centralsession.backend import SessionBackend
from tests.base import TestCase


class FlaskSessionTests(TestCase):
    REDIS_URI = 'redis://127.0.0.1:6379/1'

    def get_backend(self):
        return SessionBackend(self.REDIS_URI, key_prefix='central_session:test')

    def test_update_session(self):
        backend = self.get_backend()
        id = backend.create_session('BS_KEY', 20)
        session = backend.get_session(id)
        self.assertIsNone(session.get('test_key'))
        backend.set_key(id, 'test_key', 'yolo')
        session = backend.get_session(id)
        self.assertEqual(session.get('test_key'), 'yolo')
