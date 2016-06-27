from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from models import *

def log_in(request):
	if request.user.is_authenticated():
		return redirect(reverse('index'))
	return render(request, 'bookocr/login.html')


@login_required
def log_out(request):
	logout(request)
	return redirect(reverse('log_in'))


@login_required
def index(request):
	quote_list = Quote.objects.filter(user=request.user).order_by('-date')
	user = request.user

	context = {
		'quote_list' : quote_list,
		'user' : user,
	}
	return render(request, 'bookocr/index.html', context)


@login_required
def form(request):
	return redirect(request, 'bookocr/form.html')


@login_required
def add(request):
	q = Quote(
		user=request.user,
		book=request.POST['book'],
		date=request.POST['date'],
		photo=request.POST['photo']
		)
	q.save()

	return redirect(reverse('index'))




