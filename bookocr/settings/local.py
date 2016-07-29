#!/usr/bin/python

from django.conf import settings
from bookocr.settings import base
from bookocr.settings.base import *

# try reading local .env
no_env = os.getenv('NOENV')
env_filename = os.getenv('ENV', '.env')
if not no_env and os.path.exists(env_filename):
	print('reading local "%s" file..' % (env_filename))
	lines  = (line for line in open('.env'))
	lines  = (line.strip() for line in lines)
	lines  = (line for line in lines if line)
	tuples = (line.split('=', 1) for line in lines)
	for (key, value) in tuples:
		locals()[key] = value


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

