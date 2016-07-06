from django.test import TestCase
from django.contrib.auth.models import User

from bookshot.models import Book, Quote



class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="스토너")

    def test_Book_is_correctly_created(self):
        book = Book.objects.get(title="스토너")

        self.assertEqual(book.title, '스토너')



# QuoteTest는 2가지 버전입니다. 위의 것은 좀더 심플하고요.

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
		initial_time = quote.updated_at

		self.assertEqual(quote.user.username, 'jhk')
		self.assertEqual(quote.book.title, '열혈강호')
		self.assertEqual(quote.quotation, '봐, 나는 살아있어!')
		self.assertEqual(bool(quote.created_at), True) 
		self.assertEqual(bool(quote.updated_at), True)

		quote.quotation="아냐 그렇지 않아!"
		quote.save()

		self.assertEqual(bool(initial_time == quote.updated_at), False) 




## 아래는, 좀더 created_at, updated_at에 포커스를 두고, 
## 시간이 좀더 '적당히'' '시간스럽게' 들어갔는지 확인하기 위한, 두번째 테스트코드입니다. 


	def test_Quote_time_is_correctly_created(self):
		quote = Quote.objects.get(quotation="봐, 나는 살아있어!")
		initial_time = quote.updated_at

		self.assertEqual(quote.user.username, 'jhk')
		self.assertEqual(quote.book.title, '열혈강호')
		self.assertEqual(quote.quotation, '봐, 나는 살아있어!')
		self.assertEqual(bool(quote.created_at.day == quote.updated_at.day), True)
		self.assertEqual(bool(quote.created_at.second == quote.updated_at.second), True)

		quote.quotation = "아냐 그렇지 않아!"
		quote.save()

		self.assertEqual(bool(initial_time.microsecond == quote.updated_at.microsecond), False)


