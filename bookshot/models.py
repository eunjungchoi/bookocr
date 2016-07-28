import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.conf import settings
from django.db.models import Max

from django.conf import settings

from ocr.googlevision import detect_text

def recent_books(self):
	books = Book.objects.filter(quote__user=self).annotate(updated_at=Max('quote__updated_at')).order_by('-updated_at')
	return books

User.add_to_class("recent_books", recent_books)


class Quote(models.Model):
	quotation = models.TextField(max_length=1000)
	photo = models.ImageField(upload_to='bookshot')

	user = models.ForeignKey(User)
	book = models.ForeignKey('Book', null=True, blank=True, default=None)

	created_at = models.DateTimeField(null=True, default=None)
	updated_at = models.DateTimeField(null=True, default=None)

	def read_text_from_image(self, crop_rect, cropped_filepath=None):
		if self.photo.url.startswith('http'):
			photo_filename = self.photo.url

			# s3에서 이미지 다운받아서 image open하기
			# import boto3
			# s3 = boto3.resource('s3', 'ap-northeast-2')

			# _, filename = self.photo.name.split('/')
			# photo_filename = '{media_root}/{file_name}'.format(media_root=settings.MEDIA_ROOT, file_name=filename)
			# s3.meta.client.download_file('bookocr', 'media/{name}'.format(name=self.photo.name), photo_filename)

		else:
			photo_filename = self.photo.path

		if not cropped_filepath:
			from random import choice
			from string import ascii_uppercase

			media_root = settings.MEDIA_ROOT
			_, ext = os.path.splitext(photo_filename)
			random_string = ''.join(choice(ascii_uppercase) for i in range(10))

			cropped_filepath = '{media_root}/{random_string}{ext}'.format(**locals())

		box = (crop_rect['x'], crop_rect['y'], crop_rect['x'] + crop_rect['w'], crop_rect['y'] + crop_rect['h'])
		Quote.crop_image(photo_filename, box, cropped_filepath)

		# detect
		try:
			response = detect_text(cropped_filepath, settings=settings._wrapped)
			return response
		finally:
			if os.path.exists(cropped_filepath):
				os.remove(cropped_filepath)

	@staticmethod
	def crop_image(file_path, box, cropped_filepath):
		from PIL import Image
		import requests
		from io import StringIO, BytesIO

		if file_path.startswith('http'):
			response = requests.get(file_path)
			image = Image.open(BytesIO(response.content))
		else:
			image = Image.open(file_path)

		cropped_image = image.crop(box)

		cropped_image.save(cropped_filepath)
		return cropped_image

	@staticmethod
	def calculate_image_dimension(width, height, max_size=(640, 640)):
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


	def resize_image(self, max_size):
		from PIL import Image
		import io
		import os
		from django.core.files.uploadedfile import SimpleUploadedFile

		image = Image.open(self.photo)
		image_width, image_height = image.size
		new_width, new_height = Quote.calculate_image_dimension(image_width, image_height, max_size)

		resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

		tempfile_io = io.BytesIO()
		resized_image.save(tempfile_io, format=image.format)

		self.photo = SimpleUploadedFile(name=self.photo.name, content=tempfile_io.getvalue(), content_type='image/jpeg')


	def save(self, *args, **kwargs):
		#
		if not self.id:
			self.created_at = timezone.now()
		self.updated_at = timezone.now()

		return super(Quote, self).save(*args, **kwargs)


	def __str__(self):
		return self.quotation


class Book(models.Model):
	title = models.CharField(max_length=30)
	authors = models.CharField(max_length=100, null=False, blank=True)
	_isbn13 = models.CharField(max_length=13, null=False, blank=True, db_column="isbn13")
	cover_url = models.URLField(max_length=300, null=True, blank=True, default="")
	_raw_response = models.TextField(null=True, blank=True, default="{}")

	readers = models.ManyToManyField(User)

	# http://code.activestate.com/recipes/498104-isbn-13-converter/
	@staticmethod
	def check_digit_13th(isbn):
		assert len(isbn) == 12
		sum = 0
		for i in range(len(isbn)):
			c = int(isbn[i])
			if i % 2:
				w = 3
			else:
				w = 1
			sum += w * c
		r = 10 - (sum % 10)
		if r == 10:
			return '0'
		else:
			return str(r)


	@staticmethod
	def convert_10_to_13(isbn):
		assert len(isbn) == 10
		prefix = '978' + isbn[:-1]
		check = Book.check_digit_13th(prefix)
		return prefix + check


	@property
	def isbn13(self):
		return self._isbn13


	@isbn13.setter
	def isbn13(self, value):
		import re

		if len(value) == 10:
			self._isbn13 = Book.convert_10_to_13(value)
		else:
			self._isbn13 = value

		self._isbn13 = re.sub('[-]', '', self._isbn13)


	@property
	def raw_response(self):
		return self._raw_response


	def __str__(self):
		return self.title
