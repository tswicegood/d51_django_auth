from django.http import HttpResponse

def initiate_login(request):
    r = HttpResponse()
    r.status_code = 405
    return r
