#!/usr/bin/python

from unittest import TestCase

from ocr.googlevision import get_vision_service

from mock import MagicMock, patch, ANY, sentinel

import ocr.googlevision.text_detection


patch_discoverty_build = patch.object(ocr.googlevision.text_detection.discovery, 'build')

@patch_discoverty_build
class GetVisionServiceByDeveloperKeyTestCase(TestCase):

	def test_passing__api_key__builds_service_with_developerKey_option(self, build):
		'''passing `api_key` builds service with `developerKey` option '''
		api_key = 'ABCD1234'
		service = get_vision_service(api_key=api_key)
		#
		build.assert_called_once()
		_args, kwargs = build.call_args
		self.assertEqual(kwargs['developerKey'], api_key)

	@patch.dict('os.environ', {'GOOGLE_SERVER_APIKEY_': 'ABCD1234'})
	def test_setting_environment_variable_GOOGLE_SERVER_APIKEY___builds_service_with_developerKey_option(self, build):
		'''setting environment variable GOOGLE_SERVER_APIKEY_ builds service with `developerKey` option '''
		service = get_vision_service()
		#
		build.assert_called_once()
		_args, kwargs = build.call_args
		self.assertEqual(kwargs['developerKey'], 'ABCD1234')


@patch_discoverty_build
class GetVisionServiceByCredentialsTestCase(TestCase):

	def test_passing__credentials__builds_service_with_credentials(self, discovery_build):
		'''passing `credentials` builds service with `credentials` option '''
		service = get_vision_service(credentials=sentinel.CREDENTIALS)
		#
		_args, kwargs = discovery_build.call_args
		self.assertEqual(kwargs['credentials'], sentinel.CREDENTIALS)

	@patch.dict('os.environ', {'GOOGLE_APPLICATION_CREDENTIALS': 'credentials_file_test.json'})
	@patch.object(ocr.googlevision.text_detection.GoogleCredentials, 'get_application_default')
	def test_setting_environment_variable_GOOGLE_APPLICATION_CREDENTIALS__builds_service_with_credentials_option(self, get_app_default, build):
		'''setting environment variable GOOGLE_APPLICATION_CREDENTIALS builds service with `credentials` option '''
		get_app_default.return_value = sentinel.CREDENTIALS

		#
		service = get_vision_service()

		#
		get_app_default.assert_called_once()
		_args, kwargs = build.call_args
		self.assertEqual(kwargs['credentials'], sentinel.CREDENTIALS)


def test_proper_http_request():
	pass


