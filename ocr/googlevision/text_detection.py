#!/usr/bin/python

import os, sys
import base64
import httplib2
import pprint

from googleapiclient import discovery
from googleapiclient import errors

from oauth2client.client import GoogleCredentials

from PIL import Image
from PIL import ImageDraw

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import httplib2
httplib2.debuglevel = 2

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

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



def annotate_images(type_name, image_file, max_results=10, num_retries=3, **kwargs):
    """Uses the Vision API to detect something in the given file.  """
    batch_request = [{
        'image': { 
            'content': base64.b64encode(image_file.read()).decode('UTF-8')
        },
        'features': [{ 
            'type': type_name, 
            'maxResults': max_results,
        }]
    }]

    service = get_vision_service(**kwargs)
    request = service.images().annotate(body={
        'requests': batch_request,
    })
    response = request.execute(num_retries=num_retries)

    return response


def highlight_polygons(image, polygons):
    """Draws a polygon around the polygons, then saves to output_filename.

    Args:
      image: a file containing the image with the polygons.
      polygons: a list of polygons found in the file. This should be in the format
          returned by the Vision API.
    """
    im   = Image.open(image)
    draw = ImageDraw.Draw(im)

    for polygon in polygons:
        box = [(v['x'], v['y']) for v in polygon['boundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    del draw
    return im


def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of dicts with information about the faces in the picture.
    """

    response = annotate_images('FACE_DETECTION', face_file, max_results=max_results)
    return response['responses'][0]['faceAnnotations']


def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the faces
          have polygons drawn around them.
    """
    im = highlight_polygons(image, faces)
    im.save(output_filename)


def detect_text(image_file, max_results=5, num_retries=3, **kwargs):
    ''' see https://github.com/GoogleCloudPlatform/cloud-vision/tree/master/python/text '''
    is_filename = False
    if isinstance(image_file, str):
        image_file  = open(image_file, 'rb')
        is_filename = True

    # request
    responses = annotate_images('TEXT_DETECTION', image_file, max_results=max_results, num_retries=num_retries, **kwargs)
    #print('responses:', responses)

    if is_filename:
        image_file.close()

    return responses

    ## handle response
    #try:
    #    if 'responses' not in responses:
    #        return {}
    #    text_response = {}
    #    for filename, response in zip([image_file.name], responses['responses']):
    #        if 'error' in response:
    #            print("API Error for %s: %s" % (
    #                    filename,
    #                    response['error']['message']
    #                    if 'message' in response['error']
    #                    else ''))
    #            continue
    #        if 'textAnnotations' in response:
    #            text_response[filename] = response['textAnnotations']
    #        else:
    #            text_response[filename] = []
    #    return text_response
    #except errors.HttpError as e:
    #    print("Http Error for %s: %s" % (filename, e))
    #except KeyError as e2:
    #    print("Key error: %s" % e2)



#
# main
#
def main(input_filename=None, output_filename=None):
    if not input_filename:
        print('Usage: %s IMAGE_FILE' % (sys.argv[0], ))
        return

    with open(input_filename, 'rb') as image:
        #faces = detect_face(image)
        #print('Found %s face%s' % (len(faces), '' if len(faces) == 1 else 's'))

        #print('Writing to file %s' % output_filename)
        ## Reset the file pointer, so we can read the file again
        #image.seek(0)
        #highlight_faces(image, faces, output_filename)

        # request annotation
        result = detect_text(image)
        # save polygon on image
        polygons = result['responses'][0]['textAnnotations']
        image.seek(0)
        im = highlight_polygons(image, polygons)
        ext = os.path.splitext(input_filename)[-1]
        im.save('%s.highlight.%s' % (input_filename, ext))

        # out
        if not output_filename:
            pprint.pprint(result)
        else:
            with open(output_filename, 'w') as out:
                import json
                out.write(json.dumps(result))

if __name__ == '__main__':
    main(*sys.argv[1:3])

# vim: sts=4 et

