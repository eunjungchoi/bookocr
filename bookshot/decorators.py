from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def http_redirect(function):
    def wrap(request, *args, **kwargs):
        if request.scheme == 'https':
            return redirect('http://{0}{1}'.format(request.META['HTTP_HOST'], request.path))
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__

    return wrap
