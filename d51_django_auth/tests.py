from django.test import TestCase

from d51_django_auth.backends import FacebookConnectBackend

class TestOfFacebookConnectBackend(TestCase):
    def test_returns_none_if_request_not_passed_in(self):
        auth = FacebookConnectBackend()
        self.assertEqual(None, auth.authenticate())

