from django.shortcuts import redirect

class HttpRedirectMiddleware(object):
    def process_request(self, request):
        if request.scheme == 'https':
            return redirect('http://{0}{1}'.format(request.META['HTTP_HOST'], request.path))
        return None
