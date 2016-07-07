from unittest import TestCase
from bookshot.views.quote import calculate_size, resize_image
import os


class ImageTestCase(TestCase):
	maxDiff = None

	def setUp(self):
		pass

	def test_calculate_size(self):
		width, height = calculate_size(320, 320)
		self.assertEqual(width, 320)
		self.assertEqual(height, 320)

		width, height = calculate_size(640, 640)
		self.assertEqual(width, 640)
		self.assertEqual(height, 640)

		width, height = calculate_size(1280, 1280)
		self.assertEqual(width, 640)
		self.assertEqual(height, 640)

		width, height = calculate_size(850, 567)
		self.assertEqual(width, 640)
		self.assertEqual(height, 426)


	def test_Image_is_correctly_resized(self):
		image_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data/ritualcoffee3.jpg")
		resize_image_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data/ritualcoffee3_resize.jpg")

		resized_image = resize_image(image_filename, resize_image_filename)

		self.assertIsNotNone(resized_image)
		self.assertEqual(resized_image.width, 640)
