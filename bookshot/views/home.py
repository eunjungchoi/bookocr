from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from bookshot.models import *

@login_required
def index(request):
	quote_list = Quote.objects.filter(user=request.user).order_by('-id')
	user = request.user

	context = {
		'quote_list' : quote_list,
		'user' : user,
	}
	return render(request, 'index.html', context)


def test_index(request):
	quote_list = Quote.objects.order_by('-id')

	context = {
		'quote_list' : quote_list,
	}
	return render(request, '_client/index.html', context)
	

@login_required
def detail(request):
	pass