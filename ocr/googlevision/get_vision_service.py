#!/usr/bin/python
#!/usr/bin/python

import os

from googleapiclient import discovery, errors

from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

__all__ = ['get_vision_service']


def get_vision_service(api_key=None, credentials=None, settings=None):
	options = {}

	# explicits 
	if api_key or credentials:
		# credentials
		if credentials and not api_key: 
			if isinstance(credentials, dict): 
				credentials = _get_application_default_credential_from_dict(credentials)
			options['credentials'] = credentials
		# api_key
		elif not credentials and api_key:
			options['developerKey'] = api_key
		#
		else: raise Exception("you can't pass both api_key= and credentials=")

	# settings
	elif settings:
		api_key     = getattr(settings, 'GOOGLE_SERVER_APIKEY_', None)
		credentials = getattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS', None)
		if api_key and credentials: 
			raise Exception("you can't pass both api_key and credentials")
		# GOOGLE_APPLICATION_CREDENTIALS=
		if credentials and not api_key:
			if isinstance(credentials, dict): 
				credentials = _get_application_default_credential_from_dict(credentials)
			else:
				credentials = _get_application_default_credential_from_file(credentials)
			options['credentials'] = credentials
		# GOOGLE_SERVER_APIKEY_=
		elif api_key and not credentials:
			options['developerKey'] = api_key
		# merge keys starting with GOOGLE_APPLICATION_CREDENTIALS__
		else:
			settings_tuple = [(key, getattr(settings, key)) for key in dir(settings)]

			# build with partials
			PREFIX = 'GOOGLE_APPLICATION_CREDENTIALS__'
			cred_dict = dict((key.replace(PREFIX, '').lower(), value) for (key,value) in settings_tuple if key.startswith(PREFIX))

			#
			credentials = _get_application_default_credential_from_dict(cred_dict)
			options['credentials'] = credentials

	# read from environment variables
	else:
		# GOOGLE_SERVER_APIKEY_=
		api_key = os.environ.get('GOOGLE_SERVER_APIKEY_')
		if api_key:
			options['developerKey'] = api_key
		# default Service account keys
		else:
			# look for GOOGLE_APPLICATION_CREDENTIALS= , and others
			credentials = GoogleCredentials.get_application_default()
			options['credentials'] = credentials

	service = discovery.build('vision', 'v1', discoveryServiceUrl=DISCOVERY_URL, **options)
	return service




from oauth2client.client import _get_application_default_credential_from_file
from oauth2client.client import AUTHORIZED_USER, SERVICE_ACCOUNT, ApplicationDefaultCredentialsError, _raise_exception_for_missing_fields, GoogleCredentials

# copied from oauth2cilent/client.py
def _get_application_default_credential_from_dict(client_credentials):
	"""Build the Application Default Credentials from file."""
	credentials_type = client_credentials.get('type')
	if credentials_type == AUTHORIZED_USER:
		required_fields = set(['client_id', 'client_secret', 'refresh_token'])
	elif credentials_type == SERVICE_ACCOUNT:
		required_fields = set(['client_id', 'client_email', 'private_key_id',
			'private_key'])
	else:
		raise ApplicationDefaultCredentialsError(
				"'type' field should be defined (and have one of the '" +
				AUTHORIZED_USER + "' or '" + SERVICE_ACCOUNT + "' values)")

	missing_fields = required_fields.difference(client_credentials.keys())

	if missing_fields:
		_raise_exception_for_missing_fields(missing_fields)

	if client_credentials['type'] == AUTHORIZED_USER:
		return GoogleCredentials(
				access_token=None,
				client_id=client_credentials['client_id'],
				client_secret=client_credentials['client_secret'],
				refresh_token=client_credentials['refresh_token'],
				token_expiry=None,
				token_uri=GOOGLE_TOKEN_URI,
				user_agent='Python client library')
	else:  # client_credentials['type'] == SERVICE_ACCOUNT
		from oauth2client.service_account import _JWTAccessCredentials
		return _JWTAccessCredentials.from_json_keyfile_dict(
				client_credentials)


#def _get_application_default_credential_from_file(filename):
#	"""Build the Application Default Credentials from file."""
#	# read the credentials from the file
#	with open(filename) as file_obj:
#		import json
#		client_credentials = json.load(file_obj)
#
#	return _get_application_default_credential_from_dict(client_credentials)

