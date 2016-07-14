from django.test import TestCase
from bookshot.models import Book, Quote


class BookISBN13TestCase(TestCase):
	def test_no_isbn_is_set_to_falsey(self):
		book = Book.objects.create(title="우리 본성의 선한 천사")
		self.assertFalse(not not book.isbn13)

class BookISBN13ConversionTestCase(TestCase):
	
	def test_return_same_when_isbn13(self):
		book = Book.objects.create(title="우리 본성의 선한 천사", isbn13='9788983716897')
		self.assertEqual(book.isbn13, "9788983716897")

	def test_convert_to_isbn13_when_isbn10(self):
		book = Book.objects.create(title="스토너", isbn13='1590171993')
		self.assertEqual(book.isbn13, "9781590171998")

	def test_remove_dash_from_isbn13(self):
		book = Book.objects.create(title="반쪼가리 자작", isbn13='978-89374-62412')
		self.assertEqual(book.isbn13, "9788937462412")
