from django.template import RequestContext

class FacebookContext(RequestContext):
    # TODO: rewrite this into a proper extension of RequestContext
    #       instead of sub-classing the whole thing
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('dict'):
            kwargs['dict'] = {}
        kwargs['dict']['facebook'] = args[0].facebook
        super(FacebookContext, self).__init__(*args, **kwargs)

