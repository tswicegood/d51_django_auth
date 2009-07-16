from django.contrib.auth.models import User
from facebook import Facebook

class FacebookConnectBackend(object):
    def authenticate(self, **credentials):
        if not credentials.has_key('request'):
            return None
        request = credentials['request']
        
        if not request.facebook.check_session(request):
            return None
        
        request.user.backend = 'd51_django_auth.backends.FacebookConnectBackend'
        try:
            user = User.objects.get(username = request.facebook.uid)
        except User.DoesNotExist:
            response = request.facebook.users.getInfo([request.facebook.uid], ['name'])
            [first_name, last_name] = response[0]['name'].split(' ', 1)
            user = User()
            user.username = request.facebook.uid
            user.first_name = first_name
            user.last_name = last_name
            user.set_unusable_password()
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
