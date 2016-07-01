from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


def log_in(request):
	if request.user.is_authenticated():
		return redirect(reverse('index'))
	return render(request, 'login.html')


@login_required
def log_out(request):
	logout(request)
	return redirect(reverse('log_in'))
