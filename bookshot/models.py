import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def detect_text(*args, **kwargs):
    import json
    return json.loads('{"responses": [{"textAnnotations": [{"description": "봐, 나는 살or있어!"}]}]}')

def recent_books(self):
	books = Book.objects.filter(quote__user=self).order_by('-quote__updated_at').distinct()

	for book in books:
		quote = Quote.objects.filter(book=book).order_by('-updated_at')[0]
		book.updated_at = quote.updated_at

	return books

User.add_to_class("recent_books", recent_books)


class Quote(models.Model):
	quotation = models.TextField(max_length=1000)
	photo = models.ImageField(upload_to='bookshot')

	user = models.ForeignKey(User)
	book = models.ForeignKey('Book', null=True, blank=True, default=None)

	created_at = models.DateTimeField(null=True, default=None)
	updated_at = models.DateTimeField(null=True, default=None)

	def read_image(self, crop_rect):
		# crop
		ts = int(timezone.now().timestamp())
		cropped_filename, ext = os.path.splitext(self.photo.path)
		cropped_tag      = 'crop-{x}-{y}-{w}-{h}-{ts}'.format(**crop_rect, ts=ts)
		cropped_filepath = '{cropped_filename}.{cropped_tag}.{ext}'.format(**locals())
		#
		box = (crop_rect['x'], crop_rect['y'], crop_rect['x'] + crop_rect['w'], crop_rect['y'] + crop_rect['h'])
		Quote.crop_image(self.photo.path, cropped_filepath, box)

		# detect
		try:
			response = detect_text(cropped_filepath)
			return response
		finally:
			pass
			#os.remove(cropped_image)

	@staticmethod
	def crop_image(file_path, cropped_filepath, box):
		from PIL import Image

		image = Image.open(file_path)
		cropped_image = image.crop(box)

		if not cropped_filepath:
			ts = int(timezone.now().timestamp())
			cropped_filename, ext = os.path.splitext(file_path)
			cropped_tag      = 'crop-{x}-{y}-{w}-{h}-{ts}'.format(**crop_rect, ts=ts)
			cropped_filepath = '{cropped_filename}.{cropped_tag}{ext}'.format(**locals())

		cropped_image.save(cropped_filepath)
		return cropped_filepath

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
	cover_url = models.URLField(max_length=300, null=True, blank=True, default=None)
	_raw_response = models.TextField(null=True, blank=True, default=None)

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
		if not self._raw_response:
			return "{}"
		return self._raw_response


	def __str__(self):
		return self.title
