import os, sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import operator

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
	print len(contours)
	for i, c in enumerate(contours):
		area = cv2.contourArea(c)
		length = cv2.arcLength(c, False)
		# cv2.drawContours(out_img, contours, i, colors[i % len(colors)], 3)
		if biggest_contour is None or length > cv2.arcLength(biggest_contour, False):
			biggest_contour = c

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

def findWrist(contour):

	top_base = int(img.shape[0] * 0.25) # ESTIMATE STARTING Y
	bottom_base = int(img.shape[0] * 0.75) # ESTIMATE STARTING Y
	# left_base = int(img.shape[1] * 0.5) # ESTIMATE STARTING X

	# selected_contour_pts = [i for i in contour if i[0][1] < bottom_base and i[0][1] > top_base and i[0][0] > left_base]
	selected_contour_pts = [i for i in contour if i[0][1] < bottom_base and i[0][1] > top_base]
	flattened_selected_contour_pts = [item for sublist in selected_contour_pts for item in sublist]
	flattened_selected_contour_pts = flattened_selected_contour_pts[::2]
	derivatives = []
	for i, pt1 in enumerate(flattened_selected_contour_pts):
		cv2.circle(out_img, (pt1[0], pt1[1]), 4, colors[1], -1)
		if i < len(flattened_selected_contour_pts) - 1:
			pt2 = flattened_selected_contour_pts[i+1]
			if pt1[1] == pt2[1]:
				derivatives.append(0)
			else:
				derivatives.append(pt2[0] - pt1[0])

	wrong_val = max(abs(v) for v in derivatives)
	val = max(abs(v) for v in derivatives if abs(v) != wrong_val)
	index = -1
	if val not in derivatives:
		index = derivatives.index(-1 * val)
	else:
		index = derivatives.index(val)
	# index += 650
	print val
	print flattened_selected_contour_pts[index-1]
	print flattened_selected_contour_pts[index]
	print flattened_selected_contour_pts[index+1]
	cv2.line(out_img, (flattened_selected_contour_pts[index][0], flattened_selected_contour_pts[index][1]), (0, flattened_selected_contour_pts[index][1]), colors[2], 5)
	

	global out_img_2
	out_img_2 = img[flattened_selected_contour_pts[index][1]:img.shape[0], 0:img.shape[1]]
	# x_list = [pt[0] for pt in flattened_selected_contour_pts]
	# np_contour = np.array(x_list)
	# print np_contour
	# derivative = np.diff(np_contour)
	# better_derivatives = copy.deepcopy(derivative)

	# thresh = 500
	# val = max(abs(v) for v in derivative if abs(v) < thresh)
	# index = -1
	# if val not in derivative.tolist():
	# 	index = derivative.tolist().index(-1 * val)
	# else:
	# 	index = derivative.tolist().index(val)
	# # index, val = max(enumerate(derivative), key=operator.itemgetter(1))
	# print val
	# print flattened_selected_contour_pts[index-1]
	# print flattened_selected_contour_pts[index]
	# print flattened_selected_contour_pts[index+1]

	# cv2.circle(out_img_2, (flattened_selected_contour_pts[index][0], flattened_selected_contour_pts[index][1]), 10, colors[2], -1)
	# cv2.circle(out_img_2, (flattened_selected_contour_pts[index+1][0], flattened_selected_contour_pts[index+1][1]), 10, colors[3], -1)
	# cv2.line(out_img, (flattened_selected_contour_pts[index][0], flattened_selected_contour_pts[index][1]), (0, flattened_selected_contour_pts[index][1]), colors[2], 5)
	# horizontals = {}
	# invalid_y = set()

	# for i1, p1 in enumerate(contour):
	# 	if i1 < len(contour)-1:
	# 		p2 = contour[i1+1]

	# 		# print p1, p2

	# 		# OPENCV POINT IS Y, X
	# 		# cv2.circle(out_img, (p1[0][0], p1[0][1]), 5, (255,245,238), -1)
	# 		line_pts = get_line(p1[0][1], p1[0][0], p2[0][1], p2[0][0])

	# 		for point in line_pts:
	# 			# Y, X
	# 			cv2.circle(out_img, (point[1], point[0]), 3, (255,245,238), -1)

	# 			if point[1] not in invalid_y:
	# 				if point[1] not in horizontals:
	# 					horizontals[point[1]] = []
	# 				horizontals[point[1]].append(point[0])
	# 				if len(horizontals[point[1]]) > 2:
	# 					del horizontals[point[1]]
	# 					invalid_y.add(point[1])

				# if point[1] not in invalid_y:
				# 	if point[1] not in horizontals: 
				# 		horizontals[point[1]] = []
				# 	if len(horizontals[point[1]]) < 2 and point[0] not in horizontals[point[1]]:
				# 		horizontals[point[1]].append(point[0])
				# 	else:
				# 		# MORE THAN TWO Y HEIGHTS, DISREGARD
	 		# 			del horizontals[point[1]]
	 		# 			invalid_y.add(point[1])

	# for y, x_arr in horizontals.iteritems():
	# 	if len(x_arr) == 2:
	# 		print (y, x_arr[0])
	# 		print (y, x_arr[1])
	# 		cv2.line(out_img, (y, x_arr[0]), (y, x_arr[1]), colors[0], 2)
	# 		# return


generateHandContour()
# print 'HERES THE BIGGEST CONTOUR'
# print biggest_contour
findWrist(biggest_contour)
plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(out_img, cmap = 'gray')
plt.title('Wrist detection'), plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(out_img_2, cmap = 'gray')
plt.title('Chopped wrist'), plt.xticks([]), plt.yticks([])
plt.show()