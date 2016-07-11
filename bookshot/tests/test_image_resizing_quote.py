import os

from django.test import TestCase, override_settings, modify_settings
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile

from PIL import Image

from django.contrib.auth.models import User

from bookshot.models import Book, Quote


# TODO: use environment specific settings, 
# see http://stackoverflow.com/a/15325966/1405998
revert_aws_settings = {
	'STATIC_URL': '/static/',
	'STATICFILES_STORAGE': 'whitenoise.django.GzipManifestStaticFilesStorage',
	'MEDIA_URL':  '/media/',
	'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
}

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))

# fixture image file
IMAGE_FILEPATH = os.path.join(TEST_ROOT, 'fixtures/media/IMG_6114.jpg')


#
# for demonstration purpose. see QuotePhotoResizeTestCase below for actualy test code
@override_settings(MEDIA_ROOT=os.path.join(TEST_ROOT, 'media'), **revert_aws_settings)
class QuoteImageFieldTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user('jhk', 'jh@gggmail.com', 'jhpassword')
		book = Book.objects.create(title="스토너")
		self.quote = Quote(
			user=user,
			book=book,
			quotation="봐, 나는 살아있어!"
		)

	def tearDown(self):
		try:
			os.remove(self.quote.photo.path)
		except:
			pass

	def test_saving_photo_field_text_file(self):
		self.quote.photo = SimpleUploadedFile('best_file_eva.txt', b'these are the file contents!')
		self.quote.save()
		#print('file saved:', self.quote.photo.path)

		exists = os.path.exists(self.quote.photo.path)
		self.assertTrue(exists)
		
	def test_saving_photo_field_image_file(self):
		image_content = open(IMAGE_FILEPATH, 'rb').read()
		self.quote.photo = SimpleUploadedFile(name='IMG_6114.jpg', content=image_content, content_type='image/jpeg')
		self.quote.save()

		# open saved image
		im = Image.open(self.quote.photo.path)
		self.assertEqual(im.filename, os.path.realpath('bookshot/tests/media/bookshot/IMG_6114.jpg'))
		self.assertEqual(im.size, (3264,2448))



@override_settings(MEDIA_ROOT=os.path.join(TEST_ROOT, 'media'), **revert_aws_settings)
class QuotePhotoResizeTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user('jhk', 'jh@gggmail.com', 'jhpassword')
		book = Book.objects.create(title="스토너")
		self.quote = Quote(
			user=user,
			book=book,
			quotation="봐, 나는 살아있어!"
		)
		self.image_content = open(IMAGE_FILEPATH, 'rb').read()

	def tearDown(self):
		try:
			os.remove(self.quote.photo.path)
		except:
			pass


	def test_resize_huge_image(self):
		self.quote.photo = SimpleUploadedFile(name='IMG_6114.jpg', content=self.image_content, content_type='image/jpeg')

		# resize
		self.quote.resize_image(max_size=(640,640))
		self.quote.save()


		# verify prev state	
		from django.core.files.base import ContentFile
		big_im = Image.open(ContentFile(self.image_content))
		self.assertTrue(big_im.width  > 640)
		self.assertTrue(big_im.height > 640)


		# assert: open saved image
		small_im = Image.open(self.quote.photo.path)
		self.assertTrue(small_im.width  == 640)
		self.assertTrue(small_im.height <= 640)


