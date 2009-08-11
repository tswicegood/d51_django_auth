from django.template import RequestContext

class FacebookContext(RequestContext):
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('dict'):
            kwargs['dict'] = {}
        kwargs['dict']['facebook'] = args[0].facebook
        super(FacebookContext, self).__init__(*args, **kwargs)
