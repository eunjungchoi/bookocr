#!/usr/bin/python
# bump: 2016년 8월  2일 화요일 15시 04분 37초 KST

from django.conf import settings
from bookocr.settings import base
from bookocr.settings.base import *


DEBUG = False

INSTALLED_APPS += (
    # other apps for production site
    'whitenoise.runserver_nostatic',
)


MIDDLEWARE_CLASSES += (
	'whitenoise.middleware.WhiteNoiseMiddleware',
)


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


#
# django-storages settings
# from https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    # 'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    # 'Cache-Control': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = 'bookocr'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'ap-northeast-2' #"us-east-1"
AWS_S3_HOST = 's3-%s.amazonaws.com' % AWS_REGION
os.environ['S3_USE_SIGV4'] = 'True' # https://github.com/boto/boto/issues/2916
AWS_S3_FILE_OVERWRITE = False


# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = "https://%s/static/" % (AWS_S3_CUSTOM_DOMAIN, )

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'bookocr.s3_custom_storage.StaticStorage'

#
MEDIA_URL = "https://%s/media/" % (AWS_S3_CUSTOM_DOMAIN, )

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'bookocr.s3_custom_storage.MediaStorage'


# # The region to connect to when storing files.
# AWS_REGION = 'ap-northeast-2' #"us-east-1"

# # The S3 calling format to use to connect to the bucket.
# AWS_S3_CALLING_FORMAT = "boto.s3.connection.OrdinaryCallingFormat"

# # The host to connect to (only needed if you are using a non-AWS host)
# AWS_S3_HOST = ""

# # A prefix to add to the start of all uploaded files.
# AWS_S3_KEY_PREFIX = ""

# # Whether to enable querystring authentication for uploaded files.
# AWS_S3_BUCKET_AUTH = True

# # The expire time used to access uploaded files.
# AWS_S3_MAX_AGE_SECONDS = 60*60  # 1 hour.

# # A custom URL prefix to use for public-facing URLs for uploaded files.
# AWS_S3_PUBLIC_URL = ""

# # Whether to set the storage class of uploaded files to REDUCED_REDUNDANCY.
# AWS_S3_REDUCED_REDUNDANCY = False

# # A dictionary of additional metadata to set on the uploaded files.
# # If the value is a callable, it will be called with the path of the file on S3.
# AWS_S3_METADATA = {}

# # Whether to enable gzip compression for uploaded files.
# AWS_S3_GZIP = True

# # The S3 bucket used to store static files.
# AWS_S3_BUCKET_NAME_STATIC = ""

# # The S3 calling format to use to connect to the static bucket.
# AWS_S3_CALLING_FORMAT_STATIC = "boto.s3.connection.OrdinaryCallingFormat"

# # The host to connect to for static files (only needed if you are using a non-AWS host)
# AWS_S3_HOST_STATIC = ""

# # Whether to enable querystring authentication for static files.
# AWS_S3_BUCKET_AUTH_STATIC = False

# # A prefix to add to the start of all static files.
# AWS_S3_KEY_PREFIX_STATIC = ""

# # The expire time used to access static files.
# AWS_S3_MAX_AGE_SECONDS_STATIC = 60*60*24*365  # 1 year.

# # A custom URL prefix to use for public-facing URLs for static files.
# AWS_S3_PUBLIC_URL_STATIC = ""

# # Whether to set the storage class of static files to REDUCED_REDUNDANCY.
# AWS_S3_REDUCED_REDUNDANCY_STATIC = False

# # A dictionary of additional metadata to set on the static files.
# # If the value is a callable, it will be called with the path of the file on S3.
# AWS_S3_METADATA_STATIC = {}

# # Whether to enable gzip compression for static files.
# AWS_S3_GZIP_STATIC = True


#
# Django Compressor
#
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# follow settings done by AWS_S3_
COMPRESS_URL     = STATIC_URL
#COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_STORAGE = STATICFILES_STORAGE = 'bookocr.s3_custom_storage.CachedStaticS3BotoStorage'
COMPRESS_ROOT    = STATIC_ROOT


#
# Logging
#
LOGGING = base.LOGGING or {'loggers': {}}
#LOGGING['loggers']['bookshot.views.quote'] = {
#    'handlers': ['console'],
#    'level': 'DEBUG',
#}

