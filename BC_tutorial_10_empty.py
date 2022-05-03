# Code inspired from
# OpenCV tutorial on stereo depthmaps https://docs.opencv.org/4.5.5/dd/d53/tutorial_py_depthmap.html
# and https://learnopencv.com/introduction-to-epipolar-geometry-and-stereo-vision/
import cv2
import numpy as np
from matplotlib import pyplot as plt


# Reading the left and right images.
img_left = cv2.imread('images/tsukuba01.jpg', cv2.IMREAD_GRAYSCALE)
img_right = img = cv2.imread('images/tsukuba02.jpg', cv2.IMREAD_GRAYSCALE)


#  Set parameters needed for stereo matching
# Create a stereo computation object using StereoBM_create or StereoSGBM_create
stereo = cv2.StereoBM_create(numDisparities=64, blockSize=9)

# Calculate disparity using the chosen stereo algorithm
disp = stereo.compute(img_left, img_right).astype(np.float32)

# Normalize the disparity map in order to display it
disp = cv2.normalize(disp, 0, 255, cv2.NORM_MINMAX)

# Display the disparity map
cv2.imshow("disparity", disp)
cv2.waitKey(0)
