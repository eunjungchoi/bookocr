import os

from django.test import TestCase

from django.contrib.auth.models import User
from bookshot.models import Book, Quote


class UserRecentBooksTestCase(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user('jhk1', 'jh1@gggmail.com')
		self.book1 = Book.objects.create(title="스토너1")
		self.quote1 = Quote(
			user=self.user1,
			book=self.book1,
			quotation="봐, 나는 살아있어1")
		#
		self.book3 = Book.objects.create(title="스토너3")
		self.quote3 = Quote(
			user=self.user1,
			book=self.book3,
			quotation="봐, 나는 살아있어3")

		#
		self.user2 = User.objects.create_user('jhk2', 'jh2@gggmail.com')
		self.book2 = Book.objects.create(title="스토너2")
		self.quote2 = Quote(
			user=self.user2,
			book=self.book2,
			quotation="봐, 나는 살아있어1")

	def tearDown(self):
		pass

	def test_should_return_only_users_books(self):
		books = self.user1.recent_books()

		#
		books = list(books)
		self.assertIn(self.book1, books)
		self.assertNotIn(self.book2, books)

	def test_should_have_books_in_reverse_updated_order(self):
		books = self.user1.recent_books()

		#
		books = list(books)
		self.assertEqual(books, [self.book3, self.book1])
		self.assertGreater(books[0].updated_at, books[1].updated_at)

	def test_books_order_changes_if_updated(self):
		# re-save quote1, updating book1's updated time
		self.quote1.save()

		books = self.user1.recent_books()

		#
		books = list(books)
		self.assertEqual(books, [self.book1, self.book3])


class UserRecentBooksQuerySetTestCase(TestCase):
	def setUp(self):
		self.user  = User.objects.create_user('jhk1', 'jh1@gggmail.com')
		self.book1 = Book.objects.create(title="스토너1")
		self.book2 = Book.objects.create(title="스토너2")
		self.book3 = Book.objects.create(title="스토너3")

		# creating quote connects user and book, and updates books updated_at time
		quote1 = Quote(user=self.user, book=self.book1, quotation="1")
		quote2 = Quote(user=self.user, book=self.book2, quotation="2")
		quote3 = Quote(user=self.user, book=self.book3, quotation="3")


	def test_can_apply_queryset_methods(self):
		books = self.user.recent_books()

		# .count
		self.assertEqual(books.count(), 3)

		# .filter
		filtered = books.filter(title__contains="2")
		self.assertEqual(filtered[0], self.book2)

		# .reverse
		reversed_books = books.reverse()
		self.assertEqual(list(reversed_books), [self.book1, self.book2, self.book3])

		#
		ordered = books.order_by('-title')
		self.assertEqual(list(ordered), [self.book3, self.book2, self.book1])

		# slice
		sliced = books[0:2]
		self.assertEqual(list(sliced), [self.book3, self.book2])


	def test_is_a_queryset_instance(self):
		from django.db.models.query import QuerySet

		books = self.user.recent_books()

		self.assertIsInstance(books, QuerySet)


