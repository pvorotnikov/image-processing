#!/usr/bin/env python

# ###############################
# @author Petar Vorotnikov
# @description apply Gaussian blur
# on the red channel of an image
# ###############################

import os, sys, logging
from PIL import Image, ImageFilter

class BlurRed:

    image = None
    blur = None

    # constructor
    def __init__(self, input, blur=10):

        # open and process the image
        try:
            self.blur = blur
            self.image = Image.open(input)
            self.processImage()

        # catch io exceptions
        except IOError as exception:
            logging.error(exception);

        # catch any other exceptions
        except Exception as exception:
            logging.error(exception);


    def processImage(self):

        # split into channels
        channels = self.image.split()
        R, G, B = 0, 1, 2

        # apply Gaussian blur on the R channel
        red = channels[R].filter(ImageFilter.GaussianBlur(self.blur))

        # combine back the image
        self.image = Image.merge("RGB", (red, channels[G], channels[B]))

