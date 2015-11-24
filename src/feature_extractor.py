import os, sys
import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
from shapely.geometry import LineString
from pprint import pprint
import math

# SETUP
path = os.path.dirname(os.path.abspath(__file__ ))
path += "/../images/" + sys.argv[1]
img = cv2.imread(path)
out_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

# PARAMETERS
num_rand_lines = 3
num_lines_per_segment = 3
colors = [(255,0,0), (100,149,237), (0,255,255), (34,139,34), (255,127,36)]
dist_threshold = 500

# DATA
veins = [] # LIST OF VEINS WHERE EACH VEIN IS A LIST OF SEGMENTS CONSTITUTING VEIN
vein_features = {}
vein_features['intersections'] = {} # STORED AS VEIN_ID MAP TO (VEIN_ID, (INTERSECTION.X, INTERSECTION.Y), ANGLE, ANGLE_SUPPLEMENTARY)
vein_features['intersection_distances'] = {} 

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]
def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else: 
        return ang_deg

def generateRandomVeins():
	for line in range(0, num_rand_lines):
		lines = []
		start_x_val = random.randint(0, out_img.shape[1])
		start_y_val = random.randint(0, out_img.shape[0])
		for line in range(0, num_lines_per_segment):
			dist = dist_threshold + 1
			while dist > dist_threshold:
				end_x_val = random.randint(0, out_img.shape[1])
				end_y_val = random.randint(0, out_img.shape[0])
				a = np.array((start_x_val, start_y_val))
				b = np.array((end_x_val, end_y_val))
				dist = np.linalg.norm(a-b)
			lines.append(((start_x_val, start_y_val), (end_x_val, end_y_val)))
			start_x_val = end_x_val
			start_y_val = end_y_val
		veins.append(lines)

	for vein in veins:
		cv2.circle(out_img, (vein[0][0][0], vein[0][0][1]), 10, (255,255,0), -1)
		for index, line in enumerate(vein):
			cv2.line(out_img, (line[0][0],line[0][1]), (line[1][0], line[1][1]), colors[index], 2)

def extractIntersections():
	for index, vein in enumerate(veins):
		for index2, vein2 in enumerate(veins):
			if set(vein) != set(vein2):
				for line in vein:
					for line2 in vein2:
						line_format = LineString(list(line))
						line_2_format = LineString(list(line2))
						intersection = line_format.intersection(line_2_format)
						if not intersection.is_empty:
							if index not in vein_features['intersections']:
								vein_features['intersections'][index] = []
							angle = ang(line, line2)
							vein_features['intersections'][index].append((index2, (int(intersection.x), int(intersection.y)), angle, 180 - angle))
							cv2.circle(out_img, (int(intersection.x), int(intersection.y)), 5, (255,245,238), -1)

def extractIntersectionDistances():
	for v_id, intersections in vein_features['intersections'].iteritems():
		for intersection in intersections:
			intersection_endpoints = (v_id, intersection[0])
			intersection_point = intersection[1]
			for v_id2, intersections2 in vein_features['intersections'].iteritems():
				for intersection2 in intersections2:
					intersection2_endpoints = (v_id2, intersection2[0])
					intersection2_point = intersection2[1]
					if intersection_point != intersection2_point:					
						a = np.array(intersection_point)
						b = np.array(intersection2_point)
						dist = np.linalg.norm(a-b)
						if (intersection_endpoints, intersection_point) not in vein_features['intersection_distances']:
							vein_features['intersection_distances'][(intersection_endpoints, intersection_point)] = {}
						vein_features['intersection_distances'][(intersection_endpoints, intersection_point)][(intersection2_endpoints, intersection2_point)] = dist

generateRandomVeins()
extractIntersections()
extractIntersectionDistances()
pprint(vein_features)

plt.subplot(221),plt.imshow(out_img, cmap = 'gray')
plt.title('Vein features'), plt.xticks([]), plt.yticks([])
plt.show()



