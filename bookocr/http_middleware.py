from django.shortcuts import redirect
import logging
logger = logging.getLogger(__name__)

class HttpRedirectMiddleware(object):
    def process_request(self, request):
        if request.scheme == 'https' and request.method == "GET": #POST일때는 redirect를 하면 안됨.
            return redirect('http://{0}{1}'.format(request.META['HTTP_HOST'], request.path))
        return None
