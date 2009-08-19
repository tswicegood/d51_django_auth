from django.conf import settings
from django.http import HttpResponse
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

