from facebook import Facebook
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class FacebookUserAuthenticationMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'facebook'):
            raise ImproperlyConfigured(
                'FacebookUserAuthenticationMiddleware requires that '
                'facebook.djangofb.FacebookMiddleware.  Ensure that it is added '
                'to MIDDLEWARE_CLASSES before adding this.'
            )

        user = authenticate(request = request)
        if not user is None:
            login(request, user)

