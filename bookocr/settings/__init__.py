#!/usr/bin/python

import os

# check DJANGO_SETTINGS_MODULE
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
if settings_module == 'bookocr.settings':
    print('no DJANGO_SETTINGS_MODULE set, using default..')
    from bookocr.settings.base import *

