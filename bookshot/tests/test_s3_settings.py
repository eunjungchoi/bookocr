#!/usr/bin/python

import os
from django.test import TestCase, override_settings, modify_settings

from bookocr import s3_custom_storage

@override_settings(
	AWS_S3_FILE_OVERWRITE=True, 
	#STATICFILES_STORAGE ='bookocr.s3_custom_storage.StaticStorage',
	DEFAULT_FILE_STORAGE='bookocr.s3_custom_storage.MediaStorage'
)
class S3OverwriteMediaStorageTestCase(TestCase):
	def setUp(self):
		pass

	def test_media_storage_should_be_overwritten(self):
		import importlib
		from django.conf import settings
		module_name = '.'.join(settings.DEFAULT_FILE_STORAGE.split('.')[:-1])
		self.module = importlib.import_module(module_name)
		self.module = importlib.reload(self.module)

		storage = getattr(self.module, settings.DEFAULT_FILE_STORAGE.split('.')[-1])

		self.assertTrue(storage.file_overwrite)


