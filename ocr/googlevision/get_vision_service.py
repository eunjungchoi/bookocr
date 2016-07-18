#!/usr/bin/python
#!/usr/bin/python

import os

from googleapiclient import discovery, errors

from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

__all__ = ['get_vision_service']


def get_vision_service(api_key=None, credentials=None):
    options = {}
    # explicit credentials
    if credentials and not api_key: 
        if isinstance(credentials, dict): 
            credentials = _get_application_default_credential_from_dict(credentials)
        options['credentials'] = credentials
    # explicit api_key
    elif not credentials and api_key:
        options['developerKey'] = api_key
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


