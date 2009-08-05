from django.test import TestCase
from django.http import HttpRequest
from d51_django_auth.backends import FacebookConnectBackend
from facebook import Facebook
import mox

class TestOfFacebookConnectBackend(TestCase):
    def test_returns_none_if_request_not_passed_in(self):
        auth = FacebookConnectBackend()
        self.assertEqual(None, auth.authenticate())

    def test_returns_none_if_check_session_fails(self):
        req = mox.MockObject(HttpRequest)
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(False)
        req.facebook = facebook
        mox.Replay(facebook)
        mox.Replay(req)

        auth = FacebookConnectBackend()
        self.assertEqual(None, auth.authenticate(request = req))

        mox.Verify(facebook)
        mox.Verify(req)

