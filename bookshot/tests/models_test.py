from django.test import TestCase
from bookshot.models import Book


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="스토너")

    def test_Book_is_correctly_created(self):
        book = Book.objects.get(title="스토너")

        self.assertEqual(book.title, '스토너')