from django.test import TestCase
from bookshot.models import Book, Quote



class BookISBN13TestCase(TestCase):
	def setUp(self):
		self.book = Book.objects.create(title="우리 본성의 선한 천사", isbn13='9788983716897')


	def test_return_same_when_isbn13(self):
		self.assertEqual(self.book.isbn13, "9788983716897")



class BookISBN10TestCase(TestCase):
	def setUp(self):
		self.book = Book.objects.create(title="스토너", isbn13='1590171993')


	def test_convert_to_isbn13_when_isbn10(self):
		self.assertEqual(self.book.isbn13, "9781590171998")



class BookISBNfilterTestCase(TestCase):
	def setUp(self):
		self.book = Book.objects.create(title="반쪼가리 자작", isbn13='978-89374-62412')


	def test_remove_dash_from_isbn13(self):
		self.assertEqual(self.book.isbn13, "9788937462412")
