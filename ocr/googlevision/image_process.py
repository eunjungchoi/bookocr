#!/usr/bin/python

import os, sys
import base64
import httplib2
import pprint

from googleapiclient import errors

from PIL import Image
from PIL import ImageDraw


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


