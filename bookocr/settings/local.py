#!/usr/bin/python

from bookocr.settings.base import *

DEBUG = True

INSTALLED_APPS += (
    #'debug_toolbar', # and other apps for local development
)

#
# compressor
#
COMPRESS_ENABLED = False


#
# logging
#
LOGGING = LOGGING or {'loggers': {}}
LOGGING['loggers']['django.db.backends'] = {
	'handlers': ['console'],
	'level': 'DEBUG',
}
#LOGGING['loggers']['bookshot.views.quote'] = {
#    'handlers': ['console'],
#    'level': 'DEBUG',
#}

