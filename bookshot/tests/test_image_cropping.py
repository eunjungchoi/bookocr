import os
from unittest import TestCase

from PIL import Image

from bookshot.views.quote import crop_image

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))


class CropImageTestCase(TestCase):
	def setUp(self):
		self.image_filename = os.path.join(TEST_ROOT, "fixtures/media/ritualcoffee3.jpg")
		self.cropped_image_filename = os.path.join(TEST_ROOT, "media/ritualcoffee3_cropped.jpg")

	def tearDown(self):
		if os.path.exists(self.cropped_image_filename):
			os.remove(self.cropped_image_filename)


	def test_returns_cropped_part_from_original_image(self):
		width = 200
		height = 200
		cropped_image = crop_image(self.image_filename, self.cropped_image_filename, (0, 0, width, height))

		self.assertIsNotNone(cropped_image)
		self.assertEqual(cropped_image.size, (width, height))
