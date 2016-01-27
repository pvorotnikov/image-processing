#!/usr/bin/env python

import os, sys, logging
from PIL import Image, ImageFilter

class ImageConvolution:

    image = None

    # constructor
    def __init__(self, input):

        # open and process the image
        try:
            self.image = Image.open(input)
            self.processImage()

        # catch io exceptions
        except IOError as exception:
            logging.error(exception);

        # catch any other exceptions
        except Exception as exception:
            logging.error(exception);


    def processImage(self):

        # apply image convolution filter for edge detection

        # predefine matrix, scale and offset
        size = (3, 3)
        scale = 1
        offset = 0

        # define kernel
        # kernel = (-1, -2, -1, 0, 0, 0, 1, 2, 1)

        # -1, -2, -1
        #  0   0   0
        #  1   2   1

        # -1, 0,  1
        # -2, 0,  2
        # -1, 0,  1

        sobel_v = (1, 2, 1, 0, 0, 0, -1, -2, -1) # Sobel V
        sobel_h = (-1, 0, 1, -2, 0, 2, -1, 0, 1) # Sobel H

        img = self.image.convert("L") # convert to grayslce
        # img = img.filter(ImageFilter.GaussianBlur(1.5)) # blur the image to remove texture
        img = img.filter(ImageFilter.MedianFilter(5)) # apply median filtr to remove texture
        img1 = img.filter(ImageFilter.Kernel(size, sobel_v, scale, offset)) # apply the filter
        img2 = img.filter(ImageFilter.Kernel(size, sobel_h, scale, offset)) # apply the filter
        self.image = img1

