import os, sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

# SETUP
path = os.path.dirname(os.path.abspath(__file__ ))
path += "/../images/" + sys.argv[1]
img = cv2.imread(path)
out_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
# out_img_2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

colors = [(255,0,0), (100,149,237), (0,255,255), (34,139,34), (255,127,36)]
biggest_contour = None

def generateHandContour():
	# hand_start_left = (out_img.shape[1]/3, out_img.shape[0] - 50)
	# hand_start_right = (out_img.shape[1]/3 * 2, out_img.shape[0] - 50)

	# cv2.circle(out_img, hand_start_left, 10, (255,255,0), -1)
	# cv2.circle(out_img, hand_start_right, 10, (255,255,0), -1)
	
	lower = np.array([25, 25, 25])
	upper = np.array([255, 255, 255])
	shapeMask = cv2.inRange(img, lower, upper)
	_, contours,hierarchy=cv2.findContours(shapeMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	global biggest_contour
	for i, c in enumerate(contours):
		area = cv2.contourArea(c)
		length = cv2.arcLength(c, False)
		# cv2.drawContours(out_img, contours, i, colors[i % len(colors)], 3)
		if biggest_contour is None or length > cv2.arcLength(biggest_contour, False):
			biggest_contour = c

def findWrist(contour):
	top_base = int(img.shape[0] * 0.25) # ESTIMATE STARTING Y
	bottom_base = int(img.shape[0] * 0.75) # ESTIMATE ENDING Y

	# selected_contour_pts = [i for i in contour if i[0][1] < bottom_base and i[0][1] > top_base and i[0][0] > left_base]
	selected_contour_pts = [i for i in contour if i[0][1] <= bottom_base and i[0][1] >= top_base]
	flattened_selected_contour_pts_verbose = [item for sublist in selected_contour_pts for item in sublist]
	flattened_selected_contour_pts = flattened_selected_contour_pts_verbose[::2]
	derivatives = []
	for i, pt1 in enumerate(flattened_selected_contour_pts):
		cv2.circle(out_img, (pt1[0], pt1[1]), 4, colors[1], -1)
		if i < len(flattened_selected_contour_pts) - 1:
			pt2 = flattened_selected_contour_pts[i+1]
			if pt1[1] == pt2[1]:
				derivatives.append(0)
			else:
				derivatives.append(pt2[0] - pt1[0])

	found = [i for i, pt in enumerate(flattened_selected_contour_pts) if pt[1] == top_base]
	min_val = None
	max_val = None
	for index in found:
		if min_val is None or flattened_selected_contour_pts[index][0] < min_val:
			min_val = flattened_selected_contour_pts[index][0]
		if max_val is None or flattened_selected_contour_pts[index][0] > max_val:
			max_val = flattened_selected_contour_pts[index][0]
	thresh = (min_val + max_val) / 2
	print 'DERIVATIVE THRESHOLD: %d' % thresh

	val = max(abs(v) for v in derivatives if abs(v) < thresh)
	index = -1
	if val not in derivatives:
		index = derivatives.index(-1 * val)
	else:
		index = derivatives.index(val)
	cv2.line(out_img, (flattened_selected_contour_pts[index][0], flattened_selected_contour_pts[index][1]), (0, flattened_selected_contour_pts[index][1]), colors[2], 5)
	global out_img_2
	out_img_2 = img[flattened_selected_contour_pts[index][1]:img.shape[0], 0:img.shape[1]]


generateHandContour()
findWrist(biggest_contour)
plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(out_img, cmap = 'gray')
plt.title('Wrist detection'), plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(out_img_2, cmap = 'gray')
plt.title('Chopped wrist'), plt.xticks([]), plt.yticks([])
plt.show()