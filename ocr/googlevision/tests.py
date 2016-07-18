#!/usr/bin/python

from unittest import TestCase

from ocr.googlevision import get_vision_service

from mock import MagicMock, patch, ANY

import ocr.googlevision.text_detection

@patch.object(ocr.googlevision.text_detection.discovery, 'build')
class GetVisionServiceByDeveloperKeyTestCase(TestCase):

	def test_passing__api_key__builds_service_with_developerKey_option(self, build):
		'''passing `api_key` builds service with `developerKey` option '''
		api_key = 'ABCD1234'
		service = get_vision_service(api_key=api_key)
		#
		build.assert_called_once()
		args, kwargs = build.call_args
		self.assertEqual(kwargs['developerKey'], api_key)

	@patch.dict('os.environ', {'GOOGLE_SERVER_APIKEY_': 'ABCD1234'})
	def test_setting_environment_variable_GOOGLE_SERVER_APIKEY___builds_service_with_developerKey_option(self, build):
		'''setting environment variable GOOGLE_SERVER_APIKEY_ builds service with `developerKey` option '''

		service = get_vision_service()
		#
		build.assert_called_once()
		args, kwargs = build.call_args
		self.assertEqual(kwargs['developerKey'], 'ABCD1234')


#class GetVisionServiceByCredentialsTestCase(TestCase):
#
#	def test_passing__credentials__builds_service_with_credentials(self):
#		'''passing `credentials` builds service with `credentials` option '''
#		pass
#
#	def test_setting_environment_variable_GOOGLE_APPLICATION_CREDENTIALS__builds_service_with_credentials_option(self):
#		'''setting environment variable GOOGLE_SERVER_APIKEY_ builds service with `developerKey` option '''
#		pass
#
#
#	def test_proper_http_request(self):
#		pass

