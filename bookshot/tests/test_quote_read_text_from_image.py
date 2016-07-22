import os
from unittest import skip

from django.test import TestCase, override_settings, modify_settings
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.core.files.base import ContentFile

from mock import MagicMock, patch, ANY

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
		# create fixtures
		user = User.objects.create_user('jhk', 'jh@gggmail.com', 'jhpassword')
		book = Book.objects.create(title="스토너")
		#
		self.quote = Quote.objects.create(
			user=user,
			book=book,
			photo=SimpleUploadedFile(name='IMG_6114.jpg', content=IMAGE_CONTENT),
			quotation="봐, 나는 살아있어!")

		# stub: Quote.crop_image
		self._Quote_crop_image = Quote.crop_image
		Quote.crop_image = MagicMock(name='Quote.crop_image', return_value='cropped_image.jpg')
		# stub: detect_text
		self.patcher = patch('bookshot.models.detect_text', return_value='{text: "넌 죽었어"}')
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
		#Quote.crop_image.assert_called_with(self.quote.photo.path, {"x": 10, "y": 10, "w": 200, "h": 150})
		pos_args = Quote.crop_image.call_args[0]
		self.assertEqual(pos_args[0:2], (self.quote.photo.path, (10, 10, 210, 160)))

	def test_requests_cropped_image_to_ocr_service(self):
		self.quote.read_text_from_image({"x": 10, "y": 10, "w": 200, "h": 150})
		#
		bookshot.models.detect_text.assert_called_once()

	def test_returns_ocr_response(self):
		response = self.quote.read_text_from_image({"x": 10, "y": 10, "w": 200, "h": 150})
		#
		self.assertEqual(response, '{text: "넌 죽었어"}')

	@skip('not impl.')
	def test_saves_ocr_response(self):
		self.quote.read_text_from_image({"x": 10, "y": 10, "w": 200, "h": 150})
		#
		self.assertEqual(self.quote._ocr_reponse, '{text: "넌 죽었어"}')

	@override_settings(MEDIA_ROOT=os.path.join(TEST_ROOT, 'media'))
	def test_cropped_file_is_removed_after_call(self):
		# restore Quote.crop_image
		Quote.crop_image = self._Quote_crop_image

		# may receive cropped_filepath=
		cropped_filepath = os.path.join(TEST_ROOT, 'media/cropped_file.jpg')
		self.quote.read_text_from_image({"x": 10, "y": 10, "w": 200, "h": 150}, cropped_filepath=cropped_filepath)

		#
		self.assert_called_once_with_arg(bookshot.models.detect_text, (cropped_filepath,))
		self.assertFalse(os.path.exists(cropped_filepath))

	def assert_called_once_with_arg(self, patched_method, check_args):
		# called once
		patched_method.assert_called_once()

		#
		(args, _kwargs) = patched_method.call_args
		self.assertEqual(args, check_args)

