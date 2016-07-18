#!/usr/bin/python

import os, sys
import pprint

from .get_vision_service import get_vision_service
from .image_process import highlight_polygons

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

