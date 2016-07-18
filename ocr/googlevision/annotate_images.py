#!/usr/bin/python

import os, sys
import base64
import httplib2
import pprint

from .get_vision_service import get_vision_service

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

