from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.template import RequestContext

from bookshot import models
from bookshot.models import User, Book, Quote


@login_required
def index(request):

	if request.scheme == 'https':
		return redirect('http://{0}{1}'.format(request.META['HTTP_HOST'], request.path))

	quote_list = Quote.objects.select_related('book', 'user').order_by('-id')

	context = {
		'quote_list' : quote_list,
	}
	return render(request, 'index.html', context)

