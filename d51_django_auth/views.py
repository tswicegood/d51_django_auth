from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout as django_logout
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, HttpResponse

def facebook_login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """ Handles logging in a user from Facebook Connect

        @todo redirect on invalid login
    """
    if not hasattr(request, 'facebook'):
        raise ImproperlyConfigured(
            'd51_django_auth.views.facebook_login requires that the PyFacebook '
            'middleware (facebook.djangofb.FacebookMiddleware) be enabled in '
            'order to login.  Please add it to your site\'s MIDDLEWARE_CLASSES'
        )

    user = authenticate(request = request)
    if not user is None:
        login(request, user)

    redirect_to = request.REQUEST.get(redirect_field_name, '/')
    return HttpResponseRedirect(redirect_to)

def facebook_xd_receiver(request):
    return HttpResponse(
"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<body>
    <script src="http://static.ak.connect.facebook.com/js/api_lib/v0.4/XdCommReceiver.js" type="text/javascript"></script>
</body>
</html>""")

def facebook_logout(request, *args, **kwargs):
    """ Handles logging a user out of system after logging out of FB Connect

        This passes off to django.contrib.auth.views.logout to handle the
        Django specific pieces after it deletes the appropriate cookies
        for Facebook Connect.
    """
    response = django_logout(request, *args, **kwargs)
    response.delete_cookie("fbsetting_%s" % settings.FACEBOOK_API_KEY)
    return response

