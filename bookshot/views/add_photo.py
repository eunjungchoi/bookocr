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
def form(request):
	return render(request, 'form.html')


@login_required
def add(request):
	book_title = request.POST['book-title']

	try:
		book = Book.objects.get(title=book_title)
	except Book.DoesNotExist:
		book = Book.objects.create(
			title = book_title
		)

	q = Quote.objects.create(
		user=request.user,
		book=book,
		photo=request.FILES['photo'],
		quotation=request.POST['quotation'],
	)

	return redirect(reverse('index'))


def test_new_quote(request):
	quote_list = Quote.objects.filter(user=request.user).order_by('-date')
	user = request.user

	context = {
		'quote_list' : quote_list,
		'user' : user,
	}
	return render(request, '_client/new_quote.html', context)

