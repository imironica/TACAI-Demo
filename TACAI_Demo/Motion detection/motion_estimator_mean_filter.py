import cv2
import numpy as np
import scipy.misc

#Parameters of the algorithms
threshold = 40;
lstNumberOfElements = 150;

#Read from the webcam stream
cam = cv2.VideoCapture(0);

#Open a new window
winName = "Motion estimator Mean Filter"
cv2.namedWindow(winName)

#list of frames for the 
lstLastFrames = [];

# Read first images (for the mean filter):
index = 0;
while(index < lstNumberOfElements):
    lstLastFrames.append(cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY));
    index = index + 1;


while True:
    mediumFilter = np.matrix(lstLastFrames[0]).astype(int);
    for i in range(1,lstNumberOfElements):
        mediumFilter = np.matrix(mediumFilter) + np.matrix(lstLastFrames[i]).astype(int);
    mediumFilter = np.divide(mediumFilter, lstNumberOfElements).astype(int);

    # Read next image
    del lstLastFrames[0];
    currentFrame = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY);
    lstLastFrames.append(currentFrame);

    currentElement = np.abs(mediumFilter - currentFrame.astype(int));
  
    currentElement[currentElement < threshold] = -125;  
    currentElement[currentElement >= threshold] = 125;
    currentElement = currentElement.astype(np.int8);
    cv2.imshow( winName, currentElement );
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break

 
