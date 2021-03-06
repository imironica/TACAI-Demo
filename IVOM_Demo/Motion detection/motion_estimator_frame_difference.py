import cv2
import numpy as np
import scipy.misc
from scipy import ndimage
# Operating system libraries
import os

# Parameters
threshold = 50
useGaussianFilter = False
useMedianFilter = True
useUniformFilter = False
skipFrames = 2

showBackground = True
saveFrames = True
root = os.path.dirname(os.path.realpath(__file__)) + '\\savedFrames\\'

# Read from the webcam stream
cam = cv2.VideoCapture(0)

# Open a new window
winNameMotion = "Motion estimator frame difference"
cv2.namedWindow(winNameMotion)
if showBackground:
    winNameBackground = "Background estimator frame difference"
    cv2.namedWindow(winNameBackground)

# Read first images:
index = 0
firstFrame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

indexSave = 0
while True:

    # skip frames
    index = 0
    while index < skipFrames:
        currentFrame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        index = index + 1

    # set filters - to remove the webcam noise (median / gaussian / uniform filters);
    if useGaussianFilter == False and useMedianFilter == False and useUniformFilter == False:
        currentElement = np.abs(currentFrame.astype(int) - firstFrame.astype(int)).astype(np.uint8)
    else:
        if useMedianFilter:
            currentElement = np.abs(
                ndimage.median_filter(currentFrame, 3).astype(int) - ndimage.median_filter(firstFrame, 3).astype(
                    int)).astype(np.uint8)
        if useGaussianFilter:
            currentElement = np.abs(
                ndimage.gaussian_filter(currentFrame, 3).astype(int) - ndimage.median_filter(firstFrame, 3).astype(
                    int)).astype(np.uint8)
        if useUniformFilter:
            currentElement = np.abs(
                ndimage.uniform_filter(currentFrame, 3).astype(int) - ndimage.uniform_filter(firstFrame, 3).astype(
                    int)).astype(np.uint8)

    firstFrame = currentFrame

    # set the threshold
    currentElement[currentElement < threshold] = 0
    currentElement[currentElement >= threshold] = 255

    # show the image
    cv2.imshow(winNameMotion, currentElement)
    if showBackground:
        cv2.imshow(winNameBackground, firstFrame.astype(np.uint8))

    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winNameMotion)
        if showBackground:
            cv2.destroyWindow(winNameBackground)
        break

    # Save the image
    indexSave = indexSave + 1
    if saveFrames:
        filename = root + str(indexSave) + '.jpg'
        scipy.misc.imsave(filename, currentElement)
