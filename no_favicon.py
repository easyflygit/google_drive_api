from django.http import HttpResponsePermanentRedirect


class NoFaviconMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico':
            return HttpResponsePermanentRedirect('/')
        return self.get_response(request)