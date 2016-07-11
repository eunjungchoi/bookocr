import os

from django.test import TestCase

from django.contrib.auth.models import User
from bookshot.models import Book, Quote

from bookshot.tests.util import create_user


class UserRecentBooksTestCase(TestCase):
	def setUp(self):
		self.user1 = create_user('jhk1', 'jh1@gggmail.com')
		self.book1 = Book.objects.create(title="스토너1")
		self.quote1 = Quote(
			user=self.user1,
			book=self.book1,
			quotation="봐, 나는 살아있어1")

		self.user2 = create_user('jhk2', 'jh2@gggmail.com')
		self.book2 = Book.objects.create(title="스토너2")
		self.quote2 = Quote(
			user=self.user2,
			book=self.book2,
			quotation="봐, 나는 살아있어1")

	def tearDown(self):
		pass

	def test_should_return_only_users_books(self):
		books = self.user1.recent_books()
		#books = [self.book1] # XXX
		books = list(books)

		self.assertIn(self.book1, books)
		self.assertNotIn(self.book2, books)

	def test_should_have_books_in_reverse_updated_order(self):
		# user1 adds new quote, from book3
		book3 = Book.objects.create(title="스토너3")
		quote3 = Quote(
			user=self.user1,
			book=book3,
			quotation="봐, 나는 살아있어3")

		books = self.user1.recent_books()
		#books = [book3, self.book1] # XXX
		books = list(books)

		self.assertEqual(books, [book3, self.book1])

