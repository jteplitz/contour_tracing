import os
import sys
import cv2
from matplotlib import pyplot as plt
import math
import numpy as np

def defuzzImg(img, iterations = 20, mode = cv2.MORPH_OPEN):
    kernel = np.ones((5,5),np.uint8)
    #NOTE: I just picked 5 iterations here because it seems to be the smallest number that works on a random picture of rishi's hand...
    return cv2.morphologyEx(img, mode, kernel, iterations=iterations)

def findCentroid(img):
    M = cv2.moments(img)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx,cy

def findRoi(img, oimg):
    padding = 0
    edges = cv2.Canny(img, 150, 160)

    x,y,w,h = cv2.boundingRect(edges)
    (x1, y1) = map(lambda val: max(0, val - padding), (x, y))
    (x2, y2) = map(lambda val: val + padding, (x + w, y + h))

    x2 = min(len(edges), x2)
    y2 = min(len(edges[0]), y2)
    return oimg[y1:y2, x1:x2]

def findContourMask(img):
    img = cv2.multiply(img, np.array([3.5]))
    ret,thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    #thresh = defuzzImg(thresh, iterations = 2, mode=cv2.MORPH_CLOSE)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=lambda x: len(x))

    mask = np.zeros(img.shape, dtype=np.int8)
    cv2.drawContours(mask, [cnt], -1, 255, -1)
    return mask

basePath = os.path.dirname(os.path.abspath(__file__ ))
background = cv2.cvtColor(cv2.imread(basePath + "/../images/empty_box.jpg"), cv2.COLOR_BGR2GRAY);
path = basePath + "/../images/" + sys.argv[1]
img = cv2.imread(path)
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

subtracted = grayImg - background
defuzzed = defuzzImg(subtracted.copy(), iterations = 5)
plt.subplot(221),plt.imshow(defuzzed, cmap = 'gray')
plt.title('Subtracted'), plt.xticks([]), plt.yticks([])

roi = findRoi(defuzzed, grayImg)
plt.subplot(222),plt.imshow(roi, cmap = 'gray')
plt.title('ROI'), plt.xticks([]), plt.yticks([])

mask = findContourMask(roi.copy())

maskedImg = cv2.bitwise_and(roi,roi, mask = mask)

plt.subplot(223),plt.imshow(maskedImg, cmap = 'gray')
plt.title('Contour'), plt.xticks([]), plt.yticks([])
#plt.show() #uncomment this line to see intermediate steps
cv2.imwrite(basePath + "/" + sys.argv[2], maskedImg)
