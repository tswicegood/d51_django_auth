from django.contrib.auth.models import User

class AbstractAuthBackend(object):
    def __init__(self, user_manager = None):
        self.user_manager = user_manager
        if not self.user_manager:
            self.user_manager = User.objects

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

