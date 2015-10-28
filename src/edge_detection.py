import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

path = os.path.dirname(os.path.abspath(__file__ ))
path += "/../images/rishi_cropped.jpg"
img = cv2.imread(path)
#realEdges = cv2.Canny(img, 25, 70, apertureSize = 3, L2gradient = False)
realEdges = cv2.Canny(img, 25, 80, apertureSize = 3, L2gradient = False)
#secondEdges = cv2.Canny(realEdges, 30, 60, apertureSize = 3, L2gradient = False)


plt.subplot(221),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.subplot(222),plt.imshow(realEdges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(233),plt.imshow(secondEdges,cmap = 'gray')
#plt.title('Best Edges Image'), plt.xticks([]), plt.yticks([])

plt.show()
