from d51_django_auth.backends import AbstractAuthBackend
from django.contrib.auth.models import User
from facebook import Facebook

FACEBOOK_CONNECT_BACKEND_STRING = 'd51_django_auth.backends.FacebookConnectBackend'

class FacebookConnectBackend(AbstractAuthBackend):
    def authenticate(self, **credentials):
        if not credentials.has_key('request'):
            return None
        request = credentials['request']

        if not request.facebook.check_session(request):
            return None

        request.user.backend = FACEBOOK_CONNECT_BACKEND_STRING
        try:
            user = self.user_manager.get(username = "fb$%s" % request.facebook.uid)
        except User.DoesNotExist:
            response = request.facebook.users.getInfo([request.facebook.uid], ['name'])
            [first_name, last_name] = response[0]['name'].split(' ', 1)
            user = self.user_manager.create(username = "fb$%s" % request.facebook.uid)
            user.first_name = first_name
            user.last_name = last_name
            user.set_unusable_password()
            user.save()

        return user

