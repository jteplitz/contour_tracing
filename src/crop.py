import os
import sys
import math
from matplotlib import pyplot as plt
import numpy as np
import cv2

LEFT_SIDE = 870;
RIGHT_SIDE = 1590;
BOTTOM = 1620;
TOP = 300;

def firstCrop(img):
    return img[TOP:BOTTOM, LEFT_SIDE:RIGHT_SIDE];

def defuzzImg(img, iterations = 5):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)

def getHandMask(img):
    rows,cols = img.shape
    _,thresh = cv2.threshold(img,120,255,cv2.THRESH_BINARY_INV)
    thresh = defuzzImg(thresh, iterations = 3)
    thresh = cv2.bitwise_not(thresh)

    mask = np.zeros((rows + 2, cols + 2), np.uint8)
    #cv2.floodFill(thresh, mask, (0,0), 0)
    cv2.floodFill(thresh, mask, (cols - 1, rows - 1), 0)
    #return thresh
    return mask

# Crop img at the wrist point found in contour
def findWrist(contour):
    x, y, w, h = cv2.boundingRect(contour)
    bottomBoundary = h * 0.5
    selected_contour_pts = [i for i in contour if i[0][1] <= bottomBoundary]
    flattened_selected_contour_pts_verbose = [item for sublist in selected_contour_pts for item in sublist]
    flattened_selected_contour_pts = flattened_selected_contour_pts_verbose[::2]

    maxX = -sys.maxint
    maxY = 0
    for pt in flattened_selected_contour_pts:
        if pt[0] > maxX:
            maxX = pt[0]
            maxY = pt[1]

    return maxY

def cropAtBoundingBox(img, mask):
    top = 0
    for index, row in enumerate(np.flipud(mask)):
        if (len(np.nonzero(row)[0]) != len(row)):
            top = index
            break

    top = len(img) - top

    left = sys.maxint 
    for row in mask[0:top]:
        firstZero = 0
        for index,val in enumerate(row):
            if (val == 0):
                firstZero = index
                break
        if firstZero < left:
            left = firstZero

    print(top, left)
    return img[0: top, left: img.shape[1] - 1], mask[0: top, left: mask.shape[1] - 1]

def applyMask(img, mask):
    output = np.zeros(img.shape)
    for i,row in enumerate(mask):
        for j, val in enumerate(row):
            if val == 0:
                output[i][j] = img[i][j]
    return output

def getContour(mask):
    return cv2.findContour(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def cropImg(path):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

    croppedImg = firstCrop(img)
    mask = getHandMask(croppedImg)
    contour = getContour(mask)
    wristY = findWrist(contour)

    # Crop the mask and the image at the wrist
    mask = mask[wristY:mask.shape[0]]
    croppedImg = croppedImg[wristY:croppedImg.shape[0]]
    finalImg, mask = cropAtBoundingBox(croppedImg, mask)
    mask = mask[0:mask.shape[0], 1: mask.shape[1] - 1]
    print(mask.shape, finalImg.shape)
    finalImg = applyMask(finalImg, mask)

    #cv2.imwrite(basePath + "/../images/roi/" + sys.argv[1], croppedImg)
    return finalImg
