from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jsonfield import JSONField


class Quote(models.Model):
	quotation = models.TextField(max_length=1000)
	photo = models.ImageField(upload_to='bookshot')

	user = models.ForeignKey(User)
	book = models.ForeignKey('Book', null=True, blank=True, default=None)

	created_at = models.DateTimeField(null=True, default=None)
	updated_at = models.DateTimeField(null=True, default=None)


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


	@staticmethod
	def resize_image(file_path, resized_file_path):
		from PIL import Image

		image = Image.open(file_path)

		image_width, image_height = image.size
		new_width, new_height = Quote.calculate_image_dimension(image_width, image_height)

		resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)	
		resized_image.save(resized_file_path)

		return resized_image


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
	isbn13 = models.CharField(max_length=13, null=False, blank=True)
	cover_url = models.URLField(max_length=300, null=True, blank=True)
	_raw_response = JSONField(null=True, blank=True, default=None)

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


	def save(self, *args, **kwargs):
		import re

		if len(self.isbn13) ==10:
			self.isbn13 = Book.convert_10_to_13(self.isbn13)

		self.isbn13 = re.sub('[-]', '', self.isbn13)

		return super(Book, self).save(*args, **kwargs)


	def __str__(self):
		return self.title
