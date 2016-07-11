#!/usr/bin/python

from bookocr.settings.base import *

DEBUG = False # Django sets Debug to False, cannot override.


if not locals().get('SECRET_KEY'):
	print('setting random secret key, only for test')
	import django.utils.crypto
	SECRET_KEY = django.utils.crypto.get_random_string()


TEST_RUNNER = 'bookocr.test.runner.BookOCRTestRunner' # 'django.test.runner.DiscoverRunner'

