from datetime import date

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger(__name__)

from bookshot.models import Book, Quote



@login_required
def form(request):
	return render(request,'bookform.html')


from django.db.models import Count

@login_required
def list(request):
	books = Book.objects.annotate(Count('quote')).all()

	context = {
		"books": books,
	}

	return render(request, 'book/list.html', context)


@login_required
def show(request, book_id):
	try:
		book = Book.objects.annotate(Count('quote')).get(id=book_id)
	except Book.DoesNotExist:
		raise Http404('Cannot find book with id=%d' % book_id)

	quotes = Quote.objects.filter(book_id=book.id)

	context = {
		"book": book,
		"quotes": quotes,
	}

	return render(request, 'book/show.html', context)


@login_required
def add(request):
	title = request.POST.get('title', False)
	b = Book(
		title=title
		)
	b.save()

	return redirect(reverse('index'))


