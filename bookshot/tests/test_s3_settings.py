#!/usr/bin/python

import os
import importlib

from django.test import TestCase, override_settings, modify_settings

import storages.backends.s3boto
from bookocr import s3_custom_storage


@override_settings(
	AWS_S3_FILE_OVERWRITE=False, 
	STATICFILES_STORAGE ='bookocr.s3_custom_storage.StaticStorage',
	DEFAULT_FILE_STORAGE='bookocr.s3_custom_storage.MediaStorage'
)
class S3OverwriteMediaStorageTestCase(TestCase):
	def setUp(self):
		# s3boto.S3BotoStorage re-reads AWS_S3_FILE_OVERWRITE
		importlib.reload(storages.backends.s3boto)

	def test_media_storage_should_be_overwritten(self):
		# reload DEFAULT_FILE_STORAGE
		from django.conf import settings
		storage = import_storage(settings.DEFAULT_FILE_STORAGE)

		# assert
		self.assertFalse(storage.file_overwrite, 'file_overwrite should be False')

	def test_static_storage_should_be_overwritten(self):
		# reload STATICFILES_STORAGE
		from django.conf import settings
		storage = import_storage(settings.STATICFILES_STORAGE)

		# assert
		self.assertTrue(storage.file_overwrite, 'file_overwrite should be True')


def import_storage(full_storage_name, do_reload=True):
	# strip module_name from 'bookocr.s3_custom_storage.StaticStorage'
	module_name  = full_storage_name[:full_storage_name.rindex('.')]
	storage_name = full_storage_name[full_storage_name.rindex('.')+1:]

	module = importlib.import_module(module_name)
	if do_reload:
		module = importlib.reload(module)

	#
	storage = getattr(module, storage_name)
	return storage

