from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from datetime import date
from PIL import Image
from bookshot.models import *

def calculate_size(width, height, max_size=(640, 640)):
	max_width, max_height = max_size

	image_ratio = width / float(height)

	if width < max_width and height < max_height:
		new_width = width
		new_height = height
	elif width > height:
		new_width = max_width
		new_height = new_width / image_ratio 
	else: 
		new_height = max_height
		new_width  = new_height * image_ratio

	return int(new_width), int(new_height)


def resize_image(file_path, resized_file_path):
	from PIL import Image
	import os

	image = Image.open(file_path)

	image_width, image_height = image.size
	new_width, new_height = calculate_size(image_width, image_height)

	resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)	
	resized_image.save(resized_file_path)

	return resized_image


@login_required
def add(request):
	book, created = Book.objects.get_or_create(
		title=request.POST['book-title']
	)
	
	q = Quote.objects.create(
		user=request.user,
		book=book,
		photo=request.FILES['photo'],
		quotation=request.POST['quotation'],
	)

	resize_image(q.photo.path, q.photo.path)

	return redirect(reverse('index'))


@login_required
def new(request):
	#recent_books = request.user.recent_books()[:3]
	recent_books = ('살인자의 기억법', '스토너')

	context = {
		recent_books: recent_books,
	}
	return render(request, 'quote/new.html', context)

