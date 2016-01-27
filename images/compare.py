#!/usr/bin/env python

# ========================
# Find similar images based on color comparison
# (histogram comparison)
# ========================

import numpy as np
import os, sys, logging, math
import matplotlib.pylab as plt
from PIL import Image, ImageChops, ImageFilter

def main():

    images = []
    histograms = []
    distances = []

    # open files
    image_files = os.listdir('./')
    for image in image_files:

        try:
            img = Image.open(image).resize((300, 300))
            histogram = img.histogram()
            images.append(image)
            histograms.append(histogram)

        except IOError:
            pass

    # get distances
    query = 0

    # save the query histogram
    query_histogram_path = save_histogram(
        histograms[query], os.path.basename(images[query]))

    # create the sobel histogram
    query_sobel_histogram, query_sobel_histogram_path = apply_sobel_filters(images[query])

    for i in range(len(images)):
        if i != query:
            histogram_path = save_histogram(histograms[i], os.path.basename(images[i]))
            sobel_image_histogram, sobel_image_histogram_path = apply_sobel_filters(images[i])
            dist = 0.5 * similarity(histograms[query], histograms[i]) # the color distance is half of the total distance
            dist_sobel = 0.5 * similarity(query_sobel_histogram, sobel_image_histogram)
            distances.append(( images[i], dist, histogram_path, sobel_image_histogram_path ))

    # sort distances
    sorted_distances = sorted(distances, key=lambda x: x[1])

    # writhe results in html
    with open('output.html', 'w') as output_html:
        output_html.write('<html><head><title>Similarity</title></head><body>')
        output_html.write('<img src="{0}" height="400" />' +
            '<img src="{1}"height="400" /><hr />'.format(images[query], query_histogram_path))
        for path, distance, histogram_path, sobel_image_histogram_path in sorted_distances:
            output_html.write('<div style="display: inline-block; text-align: center;">')
            output_html.write('<img src="{0}" height="150" />'+
                '<img src={3} height="150">' +
                '<img src="{2}" height="150"/><br />{1}'.format(path, distance, histogram_path, sobel_image_histogram_path))
            output_html.write('</div>&nbsp;&nbsp;')
        output_html.write('</body></html>')


# create Sobel for an image
def apply_sobel_filters(image_path):

    # load the image again
    image = Image.open(image_path)

    # Apply median filter to the image for noise reduction
    median_filter = ImageFilter.MedianFilter(size=3)
    median_image = image.convert('L').filter(median_filter)

    # Create sobel operators
    kernel_x = [-1, 0, 1,
                -2, 0, 2,
                -1, 0, 1] # Sobel Operator X

    kernel_y = [-1, -2, -1,
                 0,  0,  0,
                 1,  2,  1] # Sobel Operator Y

    # apply sobel x
    sobel_kernel_x = ImageFilter.Kernel((3, 3), kernel_x, 1)
    sobel_image_x = median_image.filter(sobel_kernel_x)


    sobel_kernel_y = ImageFilter.Kernel((3, 3), kernel_y, 1)
    sobel_image_y = median_image.filter(sobel_kernel_y)

    # combine the two sobel images
    sobel_image = ImageChops.add(sobel_image_x, sobel_image_y)

    # apply thresholding
    threshold = 128
    sobel_image = sobel_image.point(lambda x: x < threshold and 255)

    # create the histogram of the sobel image
    sobel_image_histogram = sobel_image.histogram()
    sobel_image_histogram = normalize(sobel_image_histogram)

    # Save the histogram
    histogram_path = save_histogram(sobel_image_histogram, os.path.basename(image.filename))

    # return the the histogram itself and the histogram path
    return sobel_image_histogram, histogram_path



# Normalize a histogram
# Vector normalization
def normalize(histogram):
    np_arr = np.array(histogram)
    normalized_arr = np_arr / np.linalg.norm(np_arr)
    return normalized_arr.tolist()


# Return eucledian distance
def similarity(histogram_a, histogram_b):
    sum_distance = 0

    histogram_a = normalize(histogram_a)
    histogram_b = normalize(histogram_b)

    for i in range(len(histogram_a)):
        sum_distance += ((histogram_a[i] - histogram_b[i]) *
                         (histogram_a[i] - histogram_b[i]))
    return math.sqrt(sum_distance)



# Save the histogram
def save_histogram(histogram, output_file):
    plt.figure()
    plt.title('histogram')
    plt.xlabel('bins')
    plt.ylabel('# of px')
    plt.xlim([0, len(histogram)])
    plt.plot(normalize(histogram))
    output_path = os.path.join('histograms', output_file)
    plt.savefig(output_path)
    plt.close()
    return output_path


if __name__ == '__main__':
    main()
