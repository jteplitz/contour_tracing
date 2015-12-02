import os
#from matplotlib import pyplot as plt
import sys
import math
import numpy as np
import cv2
import c_module_mask

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

    return img[0: top, left: img.shape[1] - 1], mask[0: top, left: mask.shape[1] - 1]

def fixedCropFromWrist(img, mask, wristY):
    IMAGE_SIZE = 480
    y1 = wristY
    y2 = wristY + IMAGE_SIZE
    #x1 = (IMAGE_SIZE - img.shape[1]) / -2
    #x2 = img.shape[1] - (IMAGE_SIZE - img.shape[1]) / -2
    x1 = img.shape[1] - IMAGE_SIZE
    x2 = img.shape[1]
    return img[y1:y2, x1:x2],mask[y1:y2, x1:x2]

def applyMask(img, mask):
    output = np.zeros(img.shape)
    for i,row in enumerate(mask):
        for j, val in enumerate(row):
            if val == 0:
                output[i][j] = img[i][j]
    return output

def getContour(mask):
    _, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 1):
        return max(contours, key=lambda c: cv2.contourArea(c))
    else:
        return contours[0]

def cropImg(path):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

    croppedImg = firstCrop(img)
    mask = getHandMask(croppedImg)
    contour = getContour(mask)
    wristY = findWrist(contour)

    # Crop the mask and the image at the wrist
    #mask = mask[wristY:mask.shape[0]]
    #croppedImg = croppedImg[wristY:croppedImg.shape[0]]
    #finalImg, mask = cropAtBoundingBox(croppedImg, mask)
    finalImg,mask = fixedCropFromWrist(croppedImg, mask, wristY)
    #mask = mask[0:mask.shape[0], 1: mask.shape[1] - 1]
    #finalImg = applyMask(finalImg, mask)
    #finalImg = c_module_mask.c_apply_mask(finalImg, mask)
    finalImg = np.multiply(finalImg, np.logical_not(mask))
    #finalImg = np.bitwise_and(finalImg, cv2.bit
    #plt.subplot(221),plt.imshow(croppedImg, cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(222),plt.imshow(mask, cmap = 'gray')
    #plt.title('Mask'), plt.xticks([]), plt.yticks([])
    #plt.subplot(223),plt.imshow(finalImg, cmap = 'gray')
    #plt.title('Cropped Image'), plt.xticks([]), plt.yticks([])
    #
    #plt.show()

    #cv2.imwrite(sys.argv[1] + ".roi", croppedImg)
    return finalImg

#cropImg(sys.argv[1])
