from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class TwitterToken(models.Model):
    user = models.OneToOneField(User)
    key = models.CharField(max_length = 100)
    secret = models.CharField(max_length = 100)

    def get_oauth_token(self):
        from oauth.oauth import OAuthToken
        return OAuthToken(self.key, self.secret)

    def get_twitter(self):
        from oauthtwitter import OAuthApi
        return OAuthApi(
            settings.D51_DJANGO_AUTH['TWITTER']['CONSUMER_KEY'],
            settings.D51_DJANGO_AUTH['TWITTER']['CONSUMER_SECRET'],
            access_token = self.get_oauth_token()
        )

