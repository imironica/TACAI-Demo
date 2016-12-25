import cv2
import numpy as np
import scipy.misc
#Operating system libraries
import os, sys

#Parameters of the algorithms
threshold = 50;
lstNumberOfElements = 150;
saveFrames = True;
showBackground = False;
root = os.path.dirname(os.path.realpath(__file__)) + '\\savedFrames\\';

#Read from the webcam stream
cam = cv2.VideoCapture(0);

#Open a new window
winName = "Motion estimator Median Filter"
cv2.namedWindow(winName)

#list of frames for the 
lstFrames = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY);
lstFrames = np.expand_dims(lstFrames, axis=2);

# Read first images (for the mean filter):
index = 1;
while(index < lstNumberOfElements):
    lstFrames = np.append(lstFrames, np.expand_dims(cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY), axis=2), axis = 2);
    index = index + 1;

index = 0;
while True:
    #Compute the median filter
    mediumFilter = np.median(lstFrames, axis = 2);
    # Read next image
    currentFrame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY);
    currentElement = np.abs(mediumFilter - currentFrame.astype(int)).astype(np.uint8);
  
    currentElement[currentElement < threshold] = 0;  
    currentElement[currentElement >= threshold] = 255;

    lstFrames = np.append(lstFrames, np.expand_dims(cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY), axis=2), axis = 2);

    if(showBackground == True):
        cv2.imshow( winName,  mediumFilter.astype(np.uint8));
    else:
        cv2.imshow( winName, currentElement);
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break

    #Save the image
    index = index + 1;
    if(saveFrames == True):
        filename = root + str(index) + '.jpg';
        if(showBackground == True):
            scipy.misc.imsave(filename, mediumFilter.astype(np.uint8));
        else:
            scipy.misc.imsave(filename, currentElement);
 