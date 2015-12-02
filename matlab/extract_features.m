pkg load signal
pkg load image
pkg load statistics


addpath("/home/pi/contour_tracing/matlab")

arglist = argv();

do_bvg(arglist{1}, arglist{2});
