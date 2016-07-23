#!/usr/bin/python

from bookocr.settings.base import *

DEBUG = True

INSTALLED_APPS += (
    #'debug_toolbar', # and other apps for local development
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

