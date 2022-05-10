# Code adapted from https://docs.opencv2.org/4.5.5/da/de9/tutorial_py_epipolar_geometry.html
# and https://www.andreasjakl.com/understand-and-apply-stereo-rectification-for-depth-maps-part-2/
import cv2
import numpy as np


def drawlines(img1, img2, lines, pts1, pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


# load left and right images
imgL = cv2.imread("images/left.jpg", cv2.IMREAD_GRAYSCALE)
imgR = cv2.imread("images/right.jpg", cv2.IMREAD_GRAYSCALE)

# find the keypoints and descriptors using SIFT_create
sift_object = cv2.SIFT_create()
keypoint_one, descriptor_one = sift_object.detectAndCompute(imgL, None)
keypoint_two, descriptor_two = sift_object.detectAndCompute(imgR, None)
print('We found %d keypoints in the left image.' % len(keypoint_one))
print('We found %d keypoints in the right image.' % len(keypoint_two))

# Visualize the SIFT keypoints

keypointimage = cv2.drawKeypoints(imgL, keypoint_one, None, color=(0, 255, 0),
                                  flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
height, width, _ = keypointimage.shape
imS = cv2.resize(keypointimage, (int(height / 4), int(width / 4)))
cv2.imshow('SIFT', imS)
cv2.waitKey()

# TODO match the keypoints using a FlannBasedMatcher

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptor_one, descriptor_two, k=2)
matchesMask = [[0, 0] for i in range(len(matches))]
pts1 = []
pts2 = []
# ratio test as per Lowe's paper - only use matches with a reasonable small distance

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1, 0]
        pts2.append(keypoint_two[m.trainIdx].pt)
        pts1.append(keypoint_one[m.queryIdx].pt)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
print('We found %d matching keypoints in both images.' % len(pts1))

# Compute the Fundamental Matrix.

F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)
# We select only inlier points
pts1 = pts1[mask.ravel() == 1]
pts2 = pts2[mask.ravel() == 1]

# TODO Visualize the epilines

# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
lines1 = lines1.reshape(-1, 3)
img5, img6 = drawlines(imgL, imgR, lines1, pts1, pts2)
# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
lines2 = lines2.reshape(-1, 3)
img3, img4 = drawlines(imgR, imgL, lines2, pts2, pts1)
height, width, _ = img3.shape
imS = cv2.resize(img3, (int(height / 6), int(width / 6)))
height, width, _ = img5.shape
imSV = cv2.resize(img5, (int(height / 6), int(width / 6)))
cv2.imshow("title", np.concatenate((imS, imSV), axis=1))
cv2.waitKey(0)

