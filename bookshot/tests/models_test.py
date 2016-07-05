from django.test import TestCase
from django.contrib.auth.models import User

from bookshot.models import Book, Quote



class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="스토너")

    def test_Book_is_correctly_created(self):
        book = Book.objects.get(title="스토너")

        self.assertEqual(book.title, '스토너')




class QuoteTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user('jhk', 'jh@gggmail.com', 'jhpassword')
		book = Book.objects.create(title="열혈강호")
		Quote.objects.create(
			user=user,
			book=book,
			quotation="봐, 나는 살아있어!"
		)

	def test_Quote_is_correctly_created(self):
		quote = Quote.objects.get(quotation="봐, 나는 살아있어!")

		self.assertEqual(quote.user.username, 'jhk')
		self.assertEqual(quote.book.title, '열혈강호')
		self.assertEqual(quote.quotation, '봐, 나는 살아있어!')

