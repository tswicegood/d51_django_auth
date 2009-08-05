from django.contrib.auth.models import User, UserManager
from django.test import TestCase
from django.http import HttpRequest
from d51_django_auth.backends import FacebookConnectBackend, FACEBOOK_CONNECT_BACKEND_STRING
from facebook import Facebook
import mox
from random import randint as random

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

    def test_returns_user_if_found(self):
        random_id = random(10, 100)
        user = mox.MockObject(User)
        user_manager = mox.MockObject(UserManager)
        user_manager.get(username = random_id).AndReturn(user)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        req.facebook = facebook

        [mox.Replay(obj) for obj in [req, facebook, user, user_manager]]

        auth = FacebookConnectBackend(user_manager = user_manager)
        self.assertEqual(user, auth.authenticate(request = req))
        self.assertEqual(FACEBOOK_CONNECT_BACKEND_STRING, req.user.backend)

        [mox.Verify(obj) for obj in [req, facebook, user, user_manager]]

