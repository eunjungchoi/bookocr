import os

from django.test import TestCase, override_settings, modify_settings
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.core.files.base import ContentFile

from mock import MagicMock, patch

from PIL import Image

from django.contrib.auth.models import User

import bookshot
from bookshot.models import Book, Quote


TEST_ROOT = os.path.dirname(os.path.realpath(__file__))
# fixture image file
IMAGE_FILEPATH = os.path.join(TEST_ROOT, 'fixtures/media/IMG_6114.jpg')
IMAGE_CONTENT  = open(IMAGE_FILEPATH, 'rb').read()


@override_settings(MEDIA_ROOT=os.path.join(TEST_ROOT, 'media'))
class QuoteReadImageTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user('jhk', 'jh@gggmail.com', 'jhpassword')
		book = Book.objects.create(title="스토너")
		#
		self.quote = Quote(
			user=user,
			book=book,
			photo=SimpleUploadedFile(name='IMG_6114.jpg', content=IMAGE_CONTENT),
			quotation="봐, 나는 살아있어!"
		)

		# stub
		# stub: Quote.crop_image
		self._Quote_crop_image = Quote.crop_image
		Quote.crop_image = MagicMock(name='Quote.crop_image')
		# stub: detect_text
		self.patcher = patch('bookshot.models.detect_text')
		self.patcher.start()
		

	def tearDown(self):
		try:
			os.remove(self.quote.photo.path)
		except:
			pass

		# restore stubs
		Quote.crop_image = self._Quote_crop_image
		self.patcher.stop()


	def test_crops_image_into_given_size(self):
		self.quote.read_text_from_image({"x": 10, "y": 10, "w": 200, "h": 150})
		#
		Quote.crop_image.assert_called_once()

	def test_requests_cropped_image_to_ocr_service(self):
		self.quote.read_text_from_image({"x": 10, "y": 10, "w": 200, "h": 150})
		#
		bookshot.models.detect_text.assert_called_once()

	#def test_saves_ocr_response(self):
	#	pass

	#def test_returns_ocr_response(self):
	#	pass

