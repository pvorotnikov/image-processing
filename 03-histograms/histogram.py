#!/usr/bin/env python

import numpy as np
import os, sys, logging, math
import matplotlib.pylab as plt
from PIL import Image, ImageFilter, ImageOps

class Histogaram:

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

        histogram1 = self.image.convert('L').histogram()
        histogram2 = ImageOps.equalize(self.image.convert('L')).histogram2()

        distance = self.compareHistograms(histogram1, histogram2)


        # greyscale_image = self.image.convert('L')
        # rgb_channels = self.image.split()
        # plt_image = self.plotImageHistogram(self.image)

        # plt_greyscale = self.plotGreyscaleHistogram(greyscale_image)
        # plt_color = self.plotColorHistogram(rgb_channels)
        # plt_color.show()
        # plt_greyscale.show()

    def compareHistograms(self, histogram1, histogram2):

        sum_distance = 0
        for i in range(256):
            sum_distance += (histogram2[i] - histogram1[i]) * (histogram2[i] - histogram1[i])

        distance = math.sqrt(sum_distance)

        return distance


    def plotImageHistogram(self, image):

        histogram = image.histogram()

        plt.figure()
        plt.title('Concatenated Histogaram')
        plt.xlabel('Bins')
        plt.ylabel('# of Pixels')
        plt.xlim([0, len(histogram) - 1])

        plt.plot(histogram)

        return plt


    def plotColorHistogram(self, channels):

        plt.figure()
        plt.title('Color Histogaram')
        plt.xlabel('Bins')
        plt.ylabel('# of Pixels')
        plt.xlim([0, 255])

        for i, channel in enumerate(channels):
            grayscale_histogram = channel.histogram()
            plt.plot(grayscale_histogram)

        return plt


    def plotGreyscaleHistogram(self, image):

        plt.figure()
        plt.title('Greyscale Histogaram')
        plt.xlabel('Bins')
        plt.ylabel('# of Pixels')
        plt.xlim([0, 255])

        grayscale_histogram = image.histogram()
        plt.plot(grayscale_histogram)

        return plt

