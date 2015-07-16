from centralsession import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        self.assertEqual(__version__, '0.2.0')
