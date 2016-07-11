import os
from urllib.parse import urlparse

from django.test import TestCase, override_settings
from django.test import Client, RequestFactory

from django.core.urlresolvers import resolve, reverse
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile

from django.contrib.auth.models import AnonymousUser, User
from social.apps.django_app.default.models import UserSocialAuth

from bookshot.models import Quote, Book


def create_user(username='jhk', email='jh@gggmail.com', password='jhpassword', **kwargs):
	user = User.objects.create_user(username=username, email=email, password=password, **kwargs)
	UserSocialAuth.objects.create(user=user)
	return user


TEST_ROOT = os.path.dirname(os.path.realpath(__file__))
IMAGE_FILEPATH = os.path.join(TEST_ROOT, 'fixtures/media/IMG_6114.jpg')


class AbstractQuoteOCRUpdateTestCase(TestCase):
	def setUp(self):
		self.user = create_user()
		self.book = Book.objects.create(title="열혈강호")

		image_content = open(IMAGE_FILEPATH, 'rb').read()
		self.quote = Quote.objects.create(
			user=self.user,
			book=self.book,
			photo=SimpleUploadedFile(name='IMG_6114.jpg', content=image_content, content_type='image/jpeg')
		)

		#
		self.client.force_login(self.user)
		#


class QuoteUpdateTextTestCase(AbstractQuoteOCRUpdateTestCase):

	def setUp(self):
		super(QuoteUpdateTextTestCase, self).setUp()
		#
		self.url = reverse(viewname='put_quote', args=[self.book.id, self.quote.id])
        
	def test_allow_only_post(self):
		# GET
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 405)

	def test_update_quote(self):
		# request
		response = self.client.post(self.url, {
			'quotation': '봐, 나는 살아있어!',
			#"crop-x": 10, "crop-y": 30, "crop-w": 200, "crop-h": 150,
			#'ocr_raw_response': """{text:  '봐, 나는 살or있어'}"""
		})

		#
		self.assertNotEqual(response.status_code, 405)

		# reload book from database
		quote = Quote.objects.get(id=self.quote.id)

		# verify
		self.assertEqual(quote.quotation, '봐, 나는 살아있어!')
		#
		#self.assertEqual(json.loads(book._crop_info), { "x": 10, "y": 30, "w": 200, "h": 150 })
		#self.assertEqual(book._ocr_raw_response, "{text:  '봐, 나는 살or있어'}")


class QuoteOCRUpdateAJAXTestCase(AbstractQuoteOCRUpdateTestCase):

	def setUp(self):
		super(QuoteOCRUpdateAJAXTestCase, self).setUp()
		#
		self.url = reverse(viewname='post_quote_ocr', args=[self.book.id, self.quote.id])

	def test_allow_only_post(self):
		# GET
		data = { 
			"crop-x": 10, "crop-y": 30, "crop-w": 200, "crop-h": 150 
		}
		response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		self.assertEqual(response.status_code, 200)

	def test_contains_request_info(self):
		# AJAX request
		data = { 
			"crop-x": 10, "crop-y": 30, "crop-w": 200, "crop-h": 150 
		}
		response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		# raises error if not JSON
		jsonData = response.json()

		# verify request info
		resource_uri = urlparse(jsonData['uri']).path
		self.assertEqual(resource_uri, self.url)
		self.assertEqual(urlparse(jsonData['image_url']).path, self.quote.photo.url)
		self.assertEqual(jsonData['crop_rect'], { "x": 10, "y": 30, "w": 200, "h": 150 })

		# verify result
		self.assertEqual(jsonData['result'], {"text": "봐, 나는 살or있어!"})


