#!/usr/bin/python

import os, importlib
from django.conf import settings

# check DJANGO_SETTINGS_MODULE
if os.getenv('DJANGO_SETTINGS_MODULE') == 'bookocr.settings':

	# add BOOKOCR module for convenience
	if os.getenv('BOOKOCR'):
		module_name = 'bookocr.settings.%s' % os.getenv('BOOKOCR')
		print('loading DJANGO_SETTINGS_MODULE=%s' % module_name)
		settings_module = importlib.import_module(module_name)
		#
		names = (name for name in dir(settings_module) if name.isupper())
		tuples = ((name, getattr(settings_module, name)) for name in names)

		for (key, value) in tuples:
			locals()[key] = value
	
	# use .base
	else:
		print('no DJANGO_SETTINGS_MODULE set, using default "bookocr.settings.base"..')
		from bookocr.settings.base import *

