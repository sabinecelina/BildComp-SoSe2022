import exifread
import cv2
import numpy as np


# Define a function to compute a fraction given as string

def get_fraction(text):
    split = text.split('/')
    num_one = 0
    num_two = 0
    try:
        num_one = float(split[0])
        num_two = float(split[1])
    except Exception as e:
        print(e, ": der String kann nicht in einen Bruch konvertiert werden")
    return num_one / num_two


# Open an jpg image file in order to read out the exif data
file_name = 'images/720dgree_one.jpg'
# The "rb" mode opens the file in binary format for reading
f = open(file_name, 'rb')

# Get all Exif tags
tags = exifread.process_file(f, details=False)

# Read the EXIF FocalLength tag and compute the value from it
for tag in tags:
    if tag in 'EXIF FocalLength':
        print("tag", tag)
        print("Key:", tag, "value:", tags[tag])
        focalLength_mm = get_fraction(tags[tag].__str__())
        # print the computed focal length as float value
        print("focalLength in mm: ", focalLength_mm)

# Close the file
f.close()

# Read the file as an OpenCV image
img = cv2.imread(file_name, cv2.IMREAD_COLOR)

# Extract image resolution
width, height, _ = img.shape

# TODO Compute fx, fy, cx, cy using sensor size information as proposed here:
# http://phototour.cs.washington.edu/focal.html
# focal length in pixels = (image width in pixels) * (focal length in mm) / (CCD width in mm)
# Exemplary iPhone 8 image sensor size from https://www.dpreview.com/forums/thread/4206729 and
# https://en.wikipedia.org/wiki/Image_sensor_format#Table_of_sensor_formats_and_sizes
# Type  Diagonal (mm) 	Width (mm) 	Height (mm) 	Aspect Ratio
# 1/3"  6.00 	        4.80       	3.60        	4:3

# TODO define camera intrinsic matrix K

# TODO print(K)
