# A rather simple approach for image retrieval using image histograms and
# sobel edge detection, the output is saved in a HTML page
import os, sys, math, logging, collections
import numpy as np
import matplotlib.pylab as plt
from PIL import Image, ImageFilter


ReferenceImage = collections.namedtuple('ReferenceImage', 'path, image_histogram, sobel_histogram, np_image_histogram, np_sobel_histogram')
QUERY_IMAGE = 'mountain.jpg'
DIR_BEACH = 'beach'
DIR_CITY = 'city'
DIR_MOUNTAIN = 'mountain'
RESIZE_DIMENSIONS = (256, 256)


'''
Normalizes a given histogram making it with vector distance 1
'''
def normalize_histogram(histogram):
    np_histogram = np.array(histogram)
    normalized_histogram = np_histogram / np.linalg.norm(np_histogram)

    return normalized_histogram.tolist()

'''
Get the histogram and normalize it
so that the histogram vector length is 1
'''
def get_image_histogram(image):
    histogram = normalize_histogram(image.histogram())

    return histogram


'''
Get the sobel histogram and normalize it
so that the histogram vector length is 1
'''
def get_sobel_histogram(image):

    grayscale_image = image.convert('L')

    median_filter = ImageFilter.MedianFilter(size=3)
    median_image = grayscale_image.filter(median_filter)

    sobel_x = (-1, 0, 1,
               -2, 0, 2,
               -1, 0, 1)
    sobel_kernel_x = ImageFilter.Kernel((3, 3), sobel_x, scale=1)
    sobel_image_x = median_image.filter(sobel_kernel_x)

    sobel_y = (1, 2, 1,
               0, 0, 0,
               -1, -2, -1)
    sobel_kernel_y = ImageFilter.Kernel((3, 3), sobel_y, scale=1)
    sobel_image_y = median_image.filter(sobel_kernel_y)

    # Generate histograms for X and Y and normalize them
    sobel_histogram_x = normalize_histogram(sobel_image_x.histogram())
    sobel_histogram_y = normalize_histogram(sobel_image_y.histogram())

    # Concatenate into a single histogram
    sobel_histogram = sobel_histogram_x
    sobel_histogram.extend(sobel_histogram_y)

    return sobel_histogram



def load_image(file):

    try:
        image = Image.open(file) # load the image
        image = image.resize(RESIZE_DIMENSIONS) # resize the image
        image_histogram = get_image_histogram(image)
        sobel_histogram = get_sobel_histogram(image)

        np_image_histogram = []
        np_sobel_histogram = []
        for i in range(len(image_histogram)):
            np_image_histogram.append([i, image_histogram[i]])
        for i in range(len(sobel_histogram)):
            np_sobel_histogram.append([i, sobel_histogram[i]])


        return ReferenceImage(
            path = file,
            image_histogram = image_histogram,
            np_image_histogram = np_image_histogram,
            sobel_histogram = sobel_histogram,
            np_sobel_histogram = np_sobel_histogram
        )

    except IOError:
        return None




'''
Load all images in a given path
@param {String} path
@return {Map} images
'''
def load_images(path):

    logging.info('Loading reference images in {0}'.format(path))

    # Get all image filenames in the images directory
    filenames = os.listdir(path)

    images = {}
    np_image_histograms = []
    np_sobel_histograms = []
    for filename in filenames:
        image = load_image(os.path.join(path, filename))
        if image != None:
            images[filename] = image
            np_image_histograms = sum(np_image_histograms, image.np_image_histogram)
            np_sobel_histograms = sum(np_sobel_histograms, image.np_sobel_histogram)

    return images, np_image_histograms, np_sobel_histograms


def plot_histogram(histogram):
    plt.figure()
    plt.title('Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')
    plt.xlim([0, 767])
    plt.plot(histogram)
    plt.show()
    plt.close()


'''
Main routine
'''
def main():

    logging.basicConfig(stream=sys.stdout, format="%(message)s", level=logging.INFO)

    beaches = load_images(DIR_BEACH)
    mountains = load_images(DIR_MOUNTAIN)
    cities = load_images(DIR_CITY)

    reference = load_image(QUERY_IMAGE)



if __name__ == '__main__':
    main()
