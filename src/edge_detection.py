import cv2
import numpy as np
import sys
import os
from matplotlib import pyplot as plt
edges = None
padding = 100

def subtractPadding(val):
    return max(0, val - padding)

def addPadding(val):
    return val + padding;

def cropImage(img):
    global edges
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,70,255,cv2.THRESH_BINARY)
    contours= cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    edges = cnt
    x,y,w,h = cv2.boundingRect(cnt)
    print(x,y,x+w,y+h)
    result1 = map(subtractPadding, (x, y))
    result2 = map(addPadding, (x + w, y + h))
    result2[0] = min(len(cnt), result2[0])
    result2[1] = min(len(cnt[0]), result2[1])
    x1 = result1[0]
    y1 = result1[1]
    x2 = result2[0]
    y2 = result2[1]

    croppedImage = img[y1:y2, x1:x2]
    return croppedImage

path = os.path.dirname(os.path.abspath(__file__ ))
path += "/../images/" + sys.argv[1]
img = cv2.imread(path)


plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
croppedImage = cropImage(img)
plt.subplot(222),plt.imshow(edges, cmap="gray")
plt.title("Countour"),plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(croppedImage,cmap = 'gray')
plt.title('Cropped Image'), plt.xticks([]), plt.yticks([])

plt.show()
