#!/usr/bin/env python

# ###############################
# @author Petar Vorotnikov
# @description main image processing runner
# ###############################

import os, sys, logging, argparse
from datetime import datetime
from blur_red import BlurRed

# program constants
DEFAULT_LOGGING_FORMAT = "%(message)s"
VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s (%(filename)s:%(lineno)d)"
PROGRAM = 'image-processing'
VERSION = '1.0.0'

def main(pause_on_error=False):

    # Check what time the program started
    t1 = datetime.now()


    # Get arguments
    parser = argparse.ArgumentParser(prog=PROGRAM, description=__doc__)
    parser.add_argument('input', metavar='INPUT FILE', help="Input file")
    parser.add_argument('-o', '--output', metavar='OUTPUT FILE', help="Output file", default='output.jpg')
    parser.add_argument('-s', '--show', action='store_true', help="Show result")
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('-x', '--verbose', action='store_true', help="Enable verbose logging")
    args = parser.parse_args()


    # Set logging level
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, format=VERBOSE_LOGGING_FORMAT, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stdout, format=DEFAULT_LOGGING_FORMAT, level=logging.DEBUG)


    # Run program
    try:

        # instanciate processing class
        blur = BlurRed(args.input, 10)

        # save the file
        blur.image.save(args.output)

        # show the file
        if (args.show):
            blur.image.show()

        success = True

    except Exception as exception:
        logging.critical("Unexpected error: {0}".format(exception))
        success = False


    # Check what time the progrem ended and calculate the time
    t2 = datetime.now()
    total =  t2 - t1
    logging.info("Program complete in {0}".format(total))


    # Exit
    if success:
        sys.exit(0)
    elif pause_on_error:
        raw_input("Press enter to close.")

    sys.exit(1)


if __name__ == '__main__':
    main(pause_on_error=True)
