#!/usr/bin/python

import os, sys

from googleapiclient import errors

from .get_vision_service import get_vision_service


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

