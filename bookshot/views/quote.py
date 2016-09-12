from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.contrib import messages

from django.conf import settings

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from UniversalAnalytics import Tracker

from datetime import date, datetime
from PIL import Image
from bookshot.models import *


@login_required
def new(request):
	''' render page for new quote '''
	import json

	# book
	book = Book()
	if request.GET.get('book_id'):
		book_id = request.GET['book_id']
		book = get_object_or_404(Book, pk=book_id)

	# recent books
	recent_books = request.user.recent_books()[:3]
	recent_books = [{
		"id"    : b.id,
		"title" : b.title,
		"isbn13": b.isbn13,
		"cover_url": b.cover_url,
		"raw_response": json.loads(b.raw_response or '{}'),
	} for b in recent_books]

	context = {
		'book': book,
		'recent_books': json.dumps(recent_books),
	}
	return render(request, 'quote/new.html', context)


@login_required
def add(request):
	''' save quote with book info. quote message not added yet. '''

	# track image upload time
	if request.POST['_request_start_time_ms']:
		_rtime = int(request.POST['_request_start_time_ms'])
		time_to_upload = datetime.now().timestamp() * 1000 - _rtime
		book_title = request.POST['book-title']
		tracker = Tracker.create(settings.GOOGLE_ANALYTICS_TRACKER_ID)
		tracker.send('event', 'upload', 'image', book_title, time_to_upload);
		tracker.send('timing', 'upload', 'image', time_to_upload)
		logger.debug('%.1f s to upload image' % time_to_upload)

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
	''' render page for ocr '''
	book  = get_object_or_404(Book, pk=book_id)
	quote = get_object_or_404(Quote, pk=quote_id)

	context = {
		'book' : book,
		'quote': quote
	}

	return render(request, 'quote/crop.html', context)


@login_required
def ocr_request(request, book_id, quote_id):
	''' request OCR service for current quote '''
	quote = Quote.objects.get(id=quote_id)

	area_rect = {
		'x' : int(request.POST['crop-x']),
		'y' : int(request.POST['crop-y']),
		'w' : int(request.POST['crop-w']),
		'h' : int(request.POST['crop-h']),
	}

	response = quote.read_text_from_image(area_rect)

	json = {
		'uri' : reverse(viewname='post_quote_ocr', args=[book_id, quote_id]),
		'image_url' : quote.photo.url,
		'crop_rect' : area_rect,
		'result' : {
			'text' : response['responses'][0]['textAnnotations'][0]['description'],
		},
	}
	return JsonResponse(json)


@login_required
def ocr_update(request, book_id, quote_id):
	''' save quote message '''
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'], 'only POST method is allowed')

	if not request.POST['quotation']:
		messages.error(request, '문구를 입력해주세요')
		return redirect(reverse('new_quote_ocr', kwargs={"book_id": book_id, "quote_id": quote_id}))

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

	return redirect(reverse('book', kwargs={"book_id": book_id}))

