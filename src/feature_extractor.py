import os, sys
import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
from shapely.geometry import LineString
from pprint import pprint
import util
import parser
import argparse
import math

# PARAMETERS
num_rand_lines = 3
num_lines_per_segment = 3
colors = [(255,0,0), (100,149,237), (0,255,255), (34,139,34), (255,127,36)]
dist_threshold = 500

# DATA
vein_features = {}
vein_features['intersections'] = {} # STORED AS VEIN_ID MAP TO (VEIN_ID, (INTERSECTION.X, INTERSECTION.Y), ANGLE, ANGLE_SUPPLEMENTARY)
vein_features['intersection_distances'] = {} 
vein_features['fuzzy_grid_heatmap'] = {}
vein_features['veins'] = {}

advanced_vein_features = {}
advanced_vein_features['avg_angles'] = []
advanced_vein_features['rishi_angles'] = []
advanced_vein_features['up_down'] = []

# BUCKETING
point_buckets = 40
intersection_angle_buckets = 4
distance_buckets = 40
vein_angle_buckets = 4
advanced_angle_buckets = 4

# GRID FUZZING
fuzz_cell_dimension = 3
fuzz_cell_buckets = 2

def generateRandomVeins(out_img):
	rand_veins = []
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
		rand_veins.append(lines)
	return rand_veins

def drawVeins(veins, out_img):
	for vein in veins:
		cv2.circle(out_img, (vein[0][0][0], vein[0][0][1]), 2, (255,255,0), -1)
		for index, line in enumerate(vein):
			cv2.line(out_img, (line[0][0],line[0][1]), (line[1][0], line[1][1]), colors[index % len(colors)], 1)

def extractIntersections(veins, out_img):
	for index, vein in enumerate(veins):
		for index2, vein2 in enumerate(veins):
			if set(vein) != set(vein2):
				# TREAT AS POLYLINES

				for line in vein:
					for line2 in vein2:
						line_format = LineString(list(line))
						line_2_format = LineString(list(line2))
						intersection = line_format.intersection(line_2_format)
						if not intersection.is_empty:
							if index not in vein_features['intersections']:
								vein_features['intersections'][index] = []
							angle = math.floor(util.ang(line, line2) / intersection_angle_buckets)
							supp_angle = math.floor((180 - angle) / intersection_angle_buckets)
							x_point = int(math.floor(intersection.x)) % point_buckets
							y_point = int(math.floor(intersection.y)) % point_buckets
							vein_features['intersections'][index].append((index2, (x_point, y_point), angle, supp_angle))
							cv2.circle(out_img, (int(math.floor(intersection.x)), int(math.floor(intersection.y))), 2, (255,245,238), -1)

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
						dist = int(math.floor(np.linalg.norm(a-b))) % distance_buckets
						if (intersection_endpoints, intersection_point) not in vein_features['intersection_distances']:
							vein_features['intersection_distances'][(intersection_endpoints, intersection_point)] = {}
						vein_features['intersection_distances'][(intersection_endpoints, intersection_point)][(intersection2_endpoints, intersection2_point)] = dist

def extractGrid(veins, out_img, fuzz_cell_scale, drawLines=False):
	new_x = float(out_img.shape[1]) / float(fuzz_cell_scale)
	new_y = float(out_img.shape[0]) / float(fuzz_cell_scale)
	grid_old_to_new = {} # MAPPING OF OLD CELLS TO NEW CELLS, ACCESS AS 2D ARRAY
	new_cell_counts = {} # MAPPING OF NEW CELLS TO COUNT OF VEIN OCCURRENCES PER CELL
	print 'VEINS! %d' % len(veins)

	for x in range(0, out_img.shape[1]):
		for y in range(0, out_img.shape[0]):
			new_x_cell = math.floor(float(x) / float(fuzz_cell_scale))
			new_y_cell = math.floor(float(y) / float(fuzz_cell_scale))
			if drawLines:
				cv2.line(out_img, (int(new_x_cell*fuzz_cell_scale),0), (int(new_x_cell*fuzz_cell_scale), out_img.shape[0]), colors[4], 1)
				cv2.line(out_img, (0,int(new_y_cell*fuzz_cell_scale)), (out_img.shape[1], int(new_y_cell*fuzz_cell_scale)), colors[4], 1)
			if x not in grid_old_to_new:
				grid_old_to_new[x] = {}
			grid_old_to_new[x][y] = (new_x_cell, new_y_cell)
			new_cell_counts[(new_x_cell, new_y_cell)] = 0

	for vi, vein in enumerate(veins):
		used_grid_points = set()
		for line in vein:
			points = util.get_line(line[0][0], line[0][1], line[1][0], line[1][1])
			for point in points:
				new_cell = grid_old_to_new[point[0]][point[1]]
				if new_cell not in used_grid_points:
					new_cell_counts[new_cell] += 1
					used_grid_points.add(new_cell)

	vein_features['fuzzy_grid_heatmap'] = new_cell_counts

def extractVeinAngles(veins):
	for index, vein in enumerate(veins):
		vein_features['veins'][index] = {}
		for lindex, line in enumerate(vein):
			if lindex < len(vein)-1:
				line2 = vein[lindex+1]
				line_format = LineString(list(line))
				line_2_format = LineString(list(line2))
				intersection = line_format.intersection(line_2_format)
				if not intersection.is_empty:
					# angle = int(util.ang(line, line2))
					angle = math.floor(util.ang(line, line2) / vein_angle_buckets)
					if line not in vein_features['veins'][index]:
						vein_features['veins'][index][line] = {}
					vein_features['veins'][index][line][line2] = angle

def upDowns(fuzzy_grid_heatmap):
	ud = []
	prev_val = None
	x_itr = 0
	y_itr = 0
	start_pt = (x_itr, y_itr)
	next_pt = (x_itr+1, y_itr)

	while next_pt in fuzzy_grid_heatmap.keys():
		while next_pt in fuzzy_grid_heatmap.keys():
			start_val = fuzzy_grid_heatmap[start_pt]
			next_val = fuzzy_grid_heatmap[next_pt]
			if start_val == 1:
				start_val = 0
			if next_val == 1:
				next_val = 0
			ud.append(start_val < next_val)
			start_pt = next_pt
			next_pt = (next_pt[0]+1, next_pt[1])
		x_itr = 0
		y_itr += 1
		start_pt = (x_itr, y_itr)
		next_pt = (x_itr+1, y_itr)

	x_itr = 0
	y_itr = 0
	start_pt = (x_itr, y_itr)
	next_pt = (x_itr, y_itr+1)

	while next_pt in fuzzy_grid_heatmap.keys():
		while next_pt in fuzzy_grid_heatmap.keys():
			start_val = fuzzy_grid_heatmap[start_pt]
			next_val = fuzzy_grid_heatmap[next_pt]
			if start_val == 1:
				start_val = 0
			if next_val == 1:
				next_val = 0
			ud.append(start_val < next_val)
			start_pt = next_pt
			next_pt = (next_pt[0], next_pt[1]+1)
		x_itr += 1
		y_itr = 0
		start_pt = (x_itr, y_itr)
		next_pt = (x_itr, y_itr+1)
	
	# if next_pt in fuzzy_grid_heatmap.keys():
	# 	if prev_val == 1:
	# 		pval = 0
	# 	ud.append(pval < val)
	# for key, val in fuzzy_grid_heatmap.iteritems():
	# 	if prev_val is not None:
	# 		pval = prev_val
	# 		if prev_val == 1:
	# 			pval = 0
	# 		ud.append(pval < val)
	# 	prev_val = val
	
	return ud

def avgVeinAngles(vein_angles, buckets=False):
	avg_vein_angles = []
	for key, val in vein_angles.iteritems():
		ang_sum = 0
		count = 0
		for key2, val2 in val.iteritems():
			for key3, val3 in val2.iteritems():
				ang_sum += val3
				count+=1
		if count == 0:
			avg_vein_angles.append(0)
		else:
			ang = math.floor(ang_sum / count)
			if buckets:
				ang = math.floor((ang_sum / count) / advanced_angle_buckets)				
			avg_vein_angles.append(ang)
	return sorted(avg_vein_angles)

def completeVeinAngles(veins, buckets=False):
	complete_vein_angles = []
	length = 50
	for vein in veins:
		first_point = vein[0][0]
		last_point = vein[-1][1]
		ang = math.floor(util.ang((first_point, last_point), (first_point, (first_point[0] + length, first_point[1]))))
		if buckets:
			ang = util.ang((first_point, last_point), (first_point, (first_point[0] + length, first_point[1])))
			ang = math.floor(ang / advanced_angle_buckets)
		complete_vein_angles.append(ang)
	return sorted(complete_vein_angles)

def bvgFeatureExtractor(bvg_file, index=None, 
						intersections=False, fuzzy_grid=False, 
						vein_angles=False, avg_angles=False, rishi_angles=False, 
						up_down=False, print_features=False, print_advanced_features=False):
	veins = parser.parse_csv(bvg_file)
	dims = parser.get_dimensions(bvg_file)
	fuzz_cell_scale = dims[1] / fuzz_cell_dimension
	out_img = np.zeros((dims[1], dims[0], 3), np.uint8)
	drawVeins(veins, out_img)
	if intersections:
		extractIntersections(veins, out_img)
		extractIntersectionDistances()
	if fuzzy_grid:
		extractGrid(veins, out_img, fuzz_cell_scale, drawLines=True)
	if vein_angles:
		extractVeinAngles(veins)
	
	if avg_angles:
		advanced_vein_features['avg_angles'] = avgVeinAngles(vein_features['veins'], buckets=True)
	if rishi_angles:
		advanced_vein_features['rishi_angles'] = completeVeinAngles(veins, buckets=True)
	if up_down:
		advanced_vein_features['up_down'] = upDowns(vein_features['fuzzy_grid_heatmap'])

	if print_features:
		print 'PRINTING BASIC VEIN FEATURES:\n=====================\n'
		pprint(vein_features)
	if print_advanced_features:
		print 'PRINTING ADVANCED VEIN FEATURES:\n=====================\n'
		for key, val in advanced_vein_features.iteritems():
			print 'Key: %s : %s' % (key, ', '.join(str(i) for i in val))
	if index is not None:
		grid = int('22' + str(index))
		plt.subplot(grid),plt.imshow(out_img, cmap = 'gray')
	else:
		plt.subplot(221),plt.imshow(out_img, cmap = 'gray')
	plt.title(str(index) + '. features'), plt.xticks([]), plt.yticks([])
	

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(description='BVG!')
	argparser.add_argument('--dir', type=str, default=None)
	argparser.add_argument('--file', type=str, default=None)
	args = argparser.parse_args()
	
	uds = []
	vangs = []
	cangs = []

	if args.dir:
		nums = range(1, 4)
		for num in nums:
			print '\nSTARTING: ' + args.dir + '-' + str(num)
			path = os.path.dirname(os.path.abspath(__file__ ))
			file = path + '/' + args.dir + '/' + args.dir + '-' + str(num) + '.csv'
			bvgFeatureExtractor(file, index=num, intersections=False, fuzzy_grid=True, vein_angles=True, avg_angles=True, rishi_angles=True, up_down=True, print_advanced_features=True)
	if args.file:
		path = os.path.dirname(os.path.abspath(__file__ ))
		file = path + '/' + args.file
		bvgFeatureExtractor(file, intersections=False, fuzzy_grid=True, vein_angles=True, avg_angles=True, rishi_angles=True, up_down=True, print_advanced_features=True)

	plt.show()
	
	






