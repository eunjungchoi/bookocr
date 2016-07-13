from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from datetime import date
from PIL import Image
from bookshot.models import *



def crop_image(file_path, cropped_file_path, box):
	from PIL import Image

	image = Image.open(file_path)

	cropped_image = image.crop(box)
	cropped_image.save(cropped_file_path)

	return cropped_image


@login_required
def add(request):
	book, created = Book.objects.get_or_create(
		title=request.POST['book-title'])

	q = Quote(
		user=request.user,
		book=book,
		photo=request.FILES['photo'],
		quotation=request.POST['quotation'],
	)
	q.resize_image(max_size=(640,640))
	q.save()

# 	# TO DO 
# 	# q.isbn13 =
# 	# q.cover_url = 
# 	# q._raw_response =
# 	# q.save()
	
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

	#
	book  = get_object_or_404(Book, pk=book_id)
	quote = get_object_or_404(Quote, pk=quote_id)

	#
	q_text    = request.POST['quotation']
	crop_rect = {
		'x': request.POST['crop-x'],
		'y': request.POST['crop-y'],
		'w': request.POST['crop-w'],
		'h': request.POST['crop-h'],
	}

	# update quote
	quote.quotation = q_text
	#quote._crop_info = crop_rect
	#quote._ocr_raw_response = request.POST['ocr_raw_response']
	quote.save()

	return redirect(reverse('index'))


@login_required
def new(request):
	#recent_books = request.user.recent_books()[:3]
	recent_books = ('살인자의 기억법', '스토너')

	context = {
		'recent_books': recent_books,
	}
	return render(request, 'quote/new.html', context)

