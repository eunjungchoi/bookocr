from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Quote(models.Model):
	quotation = models.TextField(max_length=1000)
	photo = models.ImageField(upload_to='bookshot')

	user = models.ForeignKey(User)
	book = models.ForeignKey('Book', null=True, blank=True, default=None)

	created_at = models.DateTimeField(null=True, default=None)
	updated_at = models.DateTimeField(null=True, default=None)


	#
	def save(self, *args, **kwargs):
		#
		if not self.id:
			self.created_at = timezone.now()
		self.updated_at = timezone.now()

		return super(self, Quote).save(*args, **kwargs)

	def __str__(self):
		return self.quotation



class Book(models.Model):
	title = models.CharField(max_length=30)
	readers = models.ManyToManyField(User)
	
	def __str__(self):
		return self.title
