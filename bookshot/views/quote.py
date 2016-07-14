from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from datetime import date
from PIL import Image
from bookshot.models import *




@login_required
def add(request):
	try:
		book = Book.objects.get(
			title=request.POST['book-title'],
		)
	except Book.DoesNotExist:
		book = Book(
			title=request.POST['book-title'],
			authors=request.POST['book-authors'],
			cover_url =request.POST['book-cover-url'],
			_raw_response =request.POST['book-response'],
		)
		book.isbn13 = request.POST['book-isbn']
		book.save()

	q = Quote(
		user=request.user,
		book=book,
		photo=request.FILES['photo'],
		quotation=request.POST['quotation'],
	)
	q.resize_image(max_size=(640,640))
	q.save()

	return redirect(reverse('new_quote_ocr', kwargs={"book_id": book.id, "quote_id": q.id}))


@login_required
def ocr_new(request, book_id, quote_id):
	book  = get_object_or_404(Book, pk=book_id)
	quote = get_object_or_404(Quote, pk=quote_id)

	context = {
		'book' : book,
		'quote': quote
	}

	return render(request, 'quote/crop.html', context)

@login_required
def ocr_request(request, book_id, quote_id):
	pass

@login_required
def ocr_update(request, book_id, quote_id):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'], 'only POST method is allowed')

	#ocr_response = {}
	#text =  '봐, 나는 살or있어!'

	#
	book  = get_object_or_404(Book, pk=book_id)
	quote = get_object_or_404(Quote, pk=quote_id)

	#
	q_text    = request.POST['quotation']
	#crop_rect = {
	#	'x': request.POST['crop-x'],
	#	'y': request.POST['crop-y'],
	#	'w': request.POST['crop-w'],
	#	'h': request.POST['crop-h'],
	#}

	# update quote
	quote.quotation = q_text
	#quote._crop_info = crop_rect
	#quote._ocr_raw_response = request.POST['ocr_raw_response']
	quote.save()

	return redirect(reverse('index'))


@login_required
def new(request):
	from django.core.serializers import serialize
	import json

	recent_books = request.user.recent_books()[:3]
	recent_books = [{
		"id"    : b.id,
		"title" : b.title,
		"isbn13": b.isbn13,
		"cover_url": b.cover_url,
		"raw_response": json.loads(b.raw_response),
	} for b in recent_books]

	context = {
		'recent_books': json.dumps(recent_books),
	}
	return render(request, 'quote/new.html', context)
