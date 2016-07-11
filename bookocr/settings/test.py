#!/usr/bin/python

from bookocr.settings.base import *

DEBUG = False # Django sets Debug to False, cannot override.

TEST_RUNNER = 'bookocr.test.runner.BookOCRTestRunner' # 'django.test.runner.DiscoverRunner'
