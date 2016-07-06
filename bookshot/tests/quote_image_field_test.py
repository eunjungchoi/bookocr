import os

from django.test import TestCase, override_settings, modify_settings

from django.core.files.uploadedfile import SimpleUploadedFile

from django.conf import settings
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

@override_settings(
	MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'bookshot/tests/media'), 
	**revert_aws_settings)
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

	def test_saving_photo_field(self):
		self.quote.photo = SimpleUploadedFile('best_file_eva.txt', b'these are the file contents!')
		self.quote.save()
		print('file saved:', self.quote.photo.path)

		exists = os.path.exists(self.quote.photo.path)
		self.assertTrue(exists)
		

