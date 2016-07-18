#!/usr/bin/python

from unittest import TestCase

import ocr.googlevision.get_vision_service 
from ocr.googlevision.get_vision_service  import get_vision_service

from ocr.googlevision.get_vision_service import GoogleCredentials
from oauth2client.service_account import _JWTAccessCredentials

from mock import MagicMock, patch, ANY, sentinel

patch_discoverty_build = patch.object(ocr.googlevision.get_vision_service.discovery, 'build')


@patch_discoverty_build
class GetVisionServiceByArgumentTestCase(TestCase):

	def test_passing__api_key__builds_service_with_developerKey_option(self, build):
		'''passing `api_key` builds service with `developerKey` option '''
		api_key = 'ABCD1234'
		service = get_vision_service(api_key=api_key)
		#
		build.assert_called_once()
		_args, kwargs = build.call_args
		self.assertEqual(kwargs['developerKey'], api_key)

	def test_passing__credentials__builds_service_with_credentials(self, discovery_build):
		'''passing `credentials` builds service with `credentials` option '''
		service = get_vision_service(credentials=sentinel.CREDENTIALS)
		#
		_args, kwargs = discovery_build.call_args
		self.assertEqual(kwargs['credentials'], sentinel.CREDENTIALS)

	@patch.object(_JWTAccessCredentials, 'from_json_keyfile_dict')
	def test_passing__credentials__as_dict_builds_credentials(self, from_json_keyfile_dict, discovery_build):
		'''passing `credentials` as a json data builds service with credentials built '''

		fake_json_data = {
			"type": "service_account",
			"project_id": "projectid",
			"private_key_id": "12345abcdefg",
			"private_key": "-----BEGIN PRIVATE KEY-----\nABCE12334\n-----END PRIVATE KEY-----\n",
			"client_email": "projectid@projectid.iam.gserviceaccount.com",
			"client_id": "12345",
			"auth_uri": "https://accounts.google.com/o/oauth2/auth",
			"token_uri": "https://accounts.google.com/o/oauth2/token",
			"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
			"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/projectid%40projectid.iam.gserviceaccount.com"
		}
		service = get_vision_service(credentials=fake_json_data)
		#
		#_args, kwargs = discovery_build.call_args
		#self.assertIsInstance(kwargs['credentials'], GoogleCredentials)

		# cannot test actual build, it checks signature.
		from_json_keyfile_dict.assert_called_once()




@patch_discoverty_build
class GetVisionServiceByEnvionrmentVariable(TestCase):
	@patch.dict('os.environ', {'GOOGLE_SERVER_APIKEY_': 'ABCD1234'})
	def test_setting_environment_variable_GOOGLE_SERVER_APIKEY___builds_service_with_developerKey_option(self, build):
		'''setting environment variable GOOGLE_SERVER_APIKEY_ builds service with `developerKey` option '''
		service = get_vision_service()
		#
		build.assert_called_once()
		_args, kwargs = build.call_args
		self.assertEqual(kwargs['developerKey'], 'ABCD1234')

	@patch.dict('os.environ', {'GOOGLE_APPLICATION_CREDENTIALS': 'credentials_file_test.json'})
	@patch.object(GoogleCredentials, 'get_application_default')
	def test_setting_environment_variable_GOOGLE_APPLICATION_CREDENTIALS__builds_service_with_credentials_option(self, get_app_default, build):
		'''setting environment variable GOOGLE_APPLICATION_CREDENTIALS builds service with `credentials` option '''
		get_app_default.return_value = sentinel.CREDENTIALS

		#
		service = get_vision_service()

		#
		get_app_default.assert_called_once()
		_args, kwargs = build.call_args
		self.assertEqual(kwargs['credentials'], sentinel.CREDENTIALS)

