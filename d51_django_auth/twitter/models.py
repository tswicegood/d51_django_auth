from django.contrib.auth.models import User
from django.db import models

class TwitterToken(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length = 100)
    secret = models.CharField(max_length = 100)

    def get_oauth_token(self):
        from oauth.oauth import OAuthToken
        return OAuthToken(self.key, self.secret)

