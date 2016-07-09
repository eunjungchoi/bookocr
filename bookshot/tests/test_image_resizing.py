import os
from unittest import TestCase

from PIL import Image

from bookshot.views.quote import calculate_size, resize_image

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))


class CalculateSizeTestCase(TestCase):

	def test_returns_itself_if_smaller(self):
		width, height = calculate_size(320, 320)
		self.assertEqual(width, 320)
		self.assertEqual(height, 320)

	def test_returns_itself_if_same(self):
		width, height = calculate_size(640, 640)
		self.assertEqual(width, 640)
		self.assertEqual(height, 640)

	def test_returns_max_size_if_larger(self):
		width, height = calculate_size(1280, 1280)
		self.assertEqual(width, 640)
		self.assertEqual(height, 640)

	def test_keeps_ratio_of_original_size_when_landscape(self):
		width, height = calculate_size(850, 567)

		self.assertEqual(width, 640)
		self.assertEqual(height, 426)
		self.assertAlmostEqual(850/567., width/float(height), delta=0.004)

	def test_keeps_ratio_of_original_size_when_portrait(self):
		width, height = calculate_size(567, 850)

		self.assertEqual(width, 426)
		self.assertEqual(height, 640)
		self.assertAlmostEqual(567/850., width/float(height), delta=0.002)

	def test_pass_max_size_as_param(self):
		width, height = calculate_size(850, 567, max_size=(850, 850))
		self.assertEqual(width, 850)
		self.assertEqual(height, 567)



class ResizeImageTestCase(TestCase):
	def setUp(self):
		self.image_filename        = os.path.join(TEST_ROOT, "fixtures/media/ritualcoffee3.jpg")
		self.resize_image_filename = os.path.join(TEST_ROOT, "media/ritualcoffee3_resize.jpg")

	def tearDown(self):
		if os.path.exists(self.resize_image_filename):
			os.remove(self.resize_image_filename)

	def test_save_large_image_file_to_smaller_image(self):
		resized_image = resize_image(self.image_filename, self.resize_image_filename)

		image = Image.open(self.image_filename)
		self.assertTrue(image.width > 640)
		self.assertEqual(resized_image.width, 640)
		self.assertTrue(resized_image.height < 640)




