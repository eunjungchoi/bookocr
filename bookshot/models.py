from django.db import models
from django.contrib.auth.models import User




class Quote(models.Model):
	user = models.ForeignKey(User)
	# book = models.ForeignKey('Book')
	date = models.DateField()
	quotation = models.TextField(max_length=1000)
	photo = models.ImageField(upload_to='static/bookshot')

	def __str__(self):
		return self.quotation



class Book(models.Model):
	title = models.CharField(max_length=30)
	
	def __str__(self):
			return self.title

