import os, sys

path = os.path.dirname(os.path.abspath(__file__ ))
path += '/' + sys.argv[1]

def get_dimensions(path):
	with open(path) as f:
		first_line = f.readline()
		dimensions = first_line.split(",")
		return (int(dimensions[1].strip()), int(dimensions[0].strip())) # X, Y

def parse_csv(path):
	with open(path) as f:
		veins = []
		for i, line in enumerate(f):
			if i > 0:
				coords = line.split(",")
				it = iter(coords)
				prev_coord = None
				segments = []
				for val in it:
					segment = []
					sanitized = int(val.translate(None, '\n').strip())
					next_sanitized = int(next(it).translate(None, '\n').strip())
					coord = (next_sanitized, sanitized)
					if prev_coord is not None:
						segment.append(prev_coord)
						segment.append(coord)
						segment_tuple = tuple(segment)
						segments.append(segment_tuple)
					prev_coord = coord
				veins.append(segments)
		return veins

parse_csv(path)