from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from oauthtwitter import OAuthApi

def initiate_login(request):
    if request.method != 'POST':
        r = HttpResponse()
        r.status_code = 405
        return r

    oauth = OAuthApi(
        settings.D51_DJANGO_AUTH['TWITTER']['CONSUMER_KEY'],
        settings.D51_DJANGO_AUTH['TWITTER']['CONSUMER_SECRET']
    )
    request_token = oauth.getRequestToken()
    request.session['twitter_request_token'] = request_token
    
    authorization_url = oauth.getAuthorizationURL(request_token)
    return redirect(authorization_url)

def login(request, redirect_field_name = auth.REDIRECT_FIELD_NAME):
    """ handle login requests for Twitter

        TODO: There's a ton of shared functionality between this and the
        facebook.login() function.  Seems like these could be refactored into a
        callable object that has a few shared methods such as
        get_authenticate_parameters() and is_valid_login_request() and remove
        the duplication.
    """
    # TODO: check for an existing TwitterToken first

    user = auth.authenticate(
        request_token = request.session['twitter_request_token']
    )

    if not user is None:
        auth.login(request, user)

    redirect_to = request.REQUEST.get(redirect_field_name, '/')
    return HttpResponseRedirect(redirect_to)

