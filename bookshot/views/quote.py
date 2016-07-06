from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from datetime import date
from bookshot.models import *


@login_required
def add(request):
	q = Quote.objects.create(
		user=request.user,
		book=book,
		photo=request.FILES['photo'],
		quotation=request.POST['quotation'],
	)

	return redirect(reverse('index'))


@login_required
def new(request):
	#recent_books = request.user.recent_books()[:3]
	recent_books = ('살인자의 기억법', '스토너')

	context = {
		recent_books: recent_books,
	}
	return render(request, '_client/new_quote.html', context)

