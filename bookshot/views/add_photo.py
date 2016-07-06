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

def calculate_size(width, height):
	max_width, max_height = (640, 640)

	image_ratio = width / float(height)

	if width < max_width and height < max_height:
		new_width = width
		new_height = height
	elif width > height:
		new_width = max_width
		new_height = max_height / image_ratio 
	else: 
		new_height = max_height
		new_width  = max_width / image_ratio

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
def form(request):
	return render(request, 'form.html')


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


def test_new_quote(request):
	quote_list = Quote.objects.filter(user=request.user).order_by('-date')
	user = request.user

	context = {
		'quote_list' : quote_list,
		'user' : user,
	}
	return render(request, '_client/new_quote.html', context)

