import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import sys

basePath = os.path.dirname(os.path.abspath(__file__ ))
background = cv2.imread(basePath + "/../images/empty_box.jpg");

# Converts image to grayscale and applys the given threshold
def applyThreshold(img, threshold):
    singleChannel = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(singleChannel,threshold,255,cv2.THRESH_BINARY)
    return thresh

def defuzzImg(img, iterations = 20, mode = cv2.MORPH_OPEN):
    kernel = np.ones((5,5),np.uint8)
    #NOTE: I just picked 5 iterations here because it seems to be the smallest number that works on a random picture of rishi's hand...
    return cv2.morphologyEx(img, mode, kernel, iterations=iterations)

def cropImg(img):
    bgRemoved = removeBackground(img)
    padding = 0
    edges = cv2.Canny(bgRemoved, 50, 100)
    x,y,w,h = cv2.boundingRect(edges)
    (x1, y1) = map(lambda val: max(0, val - padding), (x, y))
    (x2, y2) = map(lambda val: val + padding, (x + w, y + h))

    x2 = min(len(edges), x2)
    y2 = min(len(edges[0]), y2)

    return img[y1:y2, x1:x2],edges[y1:y2, x1:x2]

# TODO: This method can't be O(n^2)
def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in xrange(row1):
        for j in xrange(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

def removeBackground(img):
    bgRemoved = img - background

    bgRemoved = applyThreshold(bgRemoved, 50)
    bgRemoved = defuzzImg(bgRemoved, iterations = 3)
    return bgRemoved

def findContour(img, edges):
    copy = img.copy()
    thresh = applyThreshold(copy, 50)
    thresh = defuzzImg(thresh, iterations = 3)
    edges = cv2.Canny(thresh, 50, 100)
    #return edges
    #defuzzed = defuzzImg(img, iterations = 3)
    #thresh = applyThreshold(img, 0)
    #thresh = defuzzImg(thresh, iterations = 5, mode = cv2.MORPH_CLOSE)
    #return thresh
    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # There could be multiple contours, so pick the largest one
    #cnt = max(contours, key=lambda x: len(x))
    cv2.drawContours(copy, contours, -1, (0,255,0), 3)
    print("Num contours", len(contours))
    return copy

path = basePath + "/../images/" + sys.argv[1]
img = cv2.imread(path)
croppedImage,edges = cropImg(img)

plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Image'), plt.xticks([]), plt.yticks([])

#plt.subplot(222),plt.imshow(edges, cmap = 'gray')
#plt.title('Edges'), plt.xticks([]), plt.yticks([])

plt.subplot(222),plt.imshow(croppedImage, cmap = 'gray')
plt.title('Cropped'), plt.xticks([]), plt.yticks([])

contours = findContour(croppedImage, edges)
plt.subplot(223),plt.imshow(contours, cmap = 'gray')
plt.title('Contour'), plt.xticks([]), plt.yticks([])

plt.show()
