from datetime import date

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from bookshot.models import Book



@login_required
def form(request):
	return render(request,'bookform.html')


@login_required
def list(request):
	books = Book.objects.all()

	for book in books:
		book.quote_count = book.quote_set.count()

	context = {
		"books": books,
	}

	return render(request, 'book/list.html', context)


@login_required
def add(request):
	title = request.POST.get('title', False)
	b = Book(
		title=title
		)
	b.save()

	return redirect(reverse('index'))


