from django.contrib.auth.models import User, UserManager
from django.test import TestCase
from django.http import HttpRequest
from d51_django_auth.backends import FacebookConnectBackend, FACEBOOK_CONNECT_BACKEND_STRING
from facebook import Facebook
import mox
from random import randint as random

# Required to mock this out sync its generated dynamically and Mox
# can't/won't create stuff just for the hell of it.
class StubUserProxy(object):
    def getInfo(self, list):
        pass

def replay_all(*args):
    [mox.Replay(obj) for obj in args]

def verify_all(*args):
    [mox.Verify(obj) for obj in args]

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

    def test_user_manager_defaults_to_main_UserManager_if_not_specified(self):
        auth = FacebookConnectBackend()
        self.assertTrue(isinstance(auth.user_manager, UserManager))

    def test_uses_custom_user_manager_if_provided(self):
        obj = object()
        auth = FacebookConnectBackend(user_manager = obj)
        self.assertEquals(obj, auth.user_manager)

    def test_returns_user_if_found(self):
        random_id = random(10, 100)
        user = mox.MockObject(User)
        user_manager = mox.MockObject(UserManager)
        user_manager.get(username = "fb:%d" % random_id).AndReturn(user)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        req.facebook = facebook

        replay_all(req, facebook, user, user_manager)

        auth = FacebookConnectBackend(user_manager = user_manager)
        self.assertEqual(user, auth.authenticate(request = req))
        self.assertEqual(FACEBOOK_CONNECT_BACKEND_STRING, req.user.backend)

        verify_all(req, facebook, user, user_manager)

    def test_returns_newly_created_user_if_not_found(self):
        random_id = random(10, 100)
        user = mox.MockObject(User)
        user.set_unusable_password()
        user.save()
        user_manager = mox.MockObject(UserManager)
        user_manager.get(username = "fb:%d" % random_id).AndRaise(User.DoesNotExist())
        user_manager.create().AndReturn(user)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        facebook.users = mox.MockObject(StubUserProxy)
        facebook.users.getInfo([random_id], ['name']).AndReturn([{"name": "Foo Barger"}])
        req.facebook = facebook

        replay_all(user, user_manager, req, facebook, facebook.users)

        auth = FacebookConnectBackend(user_manager = user_manager)
        new_user = auth.authenticate(request = req)
        self.assertTrue(isinstance(new_user, User))


class TestOfNewUsersCreatedByBackend(TestCase):
    def test_username_is_salted(self):
        random_id = random(10, 100)
        user = mox.MockObject(User)
        user.set_unusable_password()
        user.save()

        user_manager = mox.MockObject(UserManager)
        user_manager.get(username = "fb:%d" % random_id).AndRaise(User.DoesNotExist())
        user_manager.create().AndReturn(user)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        facebook.users = mox.MockObject(StubUserProxy)
        facebook.users.getInfo([random_id], ['name']).AndReturn([{"name": "Foo Barger"}])
        req.facebook = facebook

        replay_all(user, user_manager, req, facebook, facebook.users)

        auth = FacebookConnectBackend(user_manager = user_manager)
        new_user = auth.authenticate(request = req)

        self.assertEqual("fb:", new_user.username[0:3])

