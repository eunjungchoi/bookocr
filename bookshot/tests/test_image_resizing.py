import os
from unittest import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
from django.contrib.auth.models import User

from bookshot.models import Quote, Book

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))


class CalculateSizeTestCase(TestCase):

	def test_returns_itself_if_smaller(self):
		width, height = Quote.calculate_image_dimension(320, 320)
		self.assertEqual(width, 320)
		self.assertEqual(height, 320)

	def test_returns_itself_if_same(self):
		width, height = Quote.calculate_image_dimension(640, 640)
		self.assertEqual(width, 640)
		self.assertEqual(height, 640)

	def test_returns_max_size_if_larger(self):
		width, height = Quote.calculate_image_dimension(1280, 1280)
		self.assertEqual(width, 640)
		self.assertEqual(height, 640)

	def test_keeps_ratio_of_original_size_when_landscape(self):
		width, height = Quote.calculate_image_dimension(850, 567)
		self.assertEqual(width, 640)
		self.assertEqual(height, 426)
		self.assertAlmostEqual(850/567., width/float(height), delta=0.004)

	def test_keeps_ratio_of_original_size_when_portrait(self):
		width, height = Quote.calculate_image_dimension(567, 850)

		self.assertEqual(width, 426)
		self.assertEqual(height, 640)
		self.assertAlmostEqual(567/850., width/float(height), delta=0.002)

	def test_pass_max_size_as_param(self):
		width, height = Quote.calculate_image_dimension(850, 567, max_size=(850, 850))
		self.assertEqual(width, 850)
		self.assertEqual(height, 567)



class ResizeImageTestCase(TestCase):
	def setUp(self):
		
		#setting
		TEST_ROOT = os.path.dirname(os.path.realpath(__file__))
		self.IMAGE_FILEPATH = os.path.join(TEST_ROOT, 'fixtures/media/IMG_6114.jpg')

		user = User.objects.create_user('jhk', 'jh@gggmail.com', 'jhpassword')
		book = Book.objects.create(title="스토너")
		self.quote = Quote(
			user=user,
			book=book,
			quotation="봐, 나는 살아있어!"
		)
		self.image_content = open(self.IMAGE_FILEPATH, 'rb').read()


	def tearDown(self):
		try:
			os.remove(self.quote.photo.path)
		except:
			pass


	def test_save_large_image_file_to_smaller_image(self):

		self.quote.photo = SimpleUploadedFile(name='IMG_6114.jpg', content=self.image_content, content_type='image/jpeg')
		self.quote.resize_image(max_size=(640,640))
		self.quote.save()

		image = Image.open(self.IMAGE_FILEPATH)
		self.assertTrue(image.width > 640)
		self.assertEqual(self.quote.photo.width, 640)
		self.assertTrue(self.quote.photo.height < 640)


