% TODO: Ideally we should get rid of this file and add tests in the cpp files directly, but 
% it's probably not worth it right now

%!test
%! ## 5 y values (same as default span)
%! y = [42 7 34 5 9];
%! yy2    = y;
%! yy2(2) = (y(1) + y(2) + y(3))/3;
%! yy2(3) = (y(1) + y(2) + y(3) + y(4) + y(5))/5;
%! yy2(4) = (y(3) + y(4) + y(5))/3;
%! yy = cpp_smooth (y, 5);
%! assert (yy, yy2);

%!test
%! ## span provided
%! y = [42 7 34 5 9];
%! yy2    = y;
%! yy2(2) = (y(1) + y(2) + y(3))/3;
%! yy2(3) = (y(2) + y(3) + y(4))/3;
%! yy2(4) = (y(3) + y(4) + y(5))/3;
%! yy = cpp_smooth (y, 3);
%! assert (yy, yy2);

%!test
%! ## random values with odd span
%! y = rand(500, 1);
%! yy = cpp_smooth(y, 9);
%! yy2 = octave_smooth(y, 9);
%! assert(yy, yy2, 1 * 10 ^-9);

%!test
%! ## cpp_vote should be equivalent to vote
%! pkg load image
%! filename = '~/contour_tracing/images/jason.crop.1447554716.jpg';
%! image = imread(filename);
%! if(ndims(image) > 2)    
%!   img_gray = rgb2gray(image);
%! else
%!   img_gray = image;
%! end
%! 
%! fil_img = uint8(imfilter(double(img_gray), ones(20) / 400, 'replicate'));
%! fil = im2double(fil_img);
%! vein_x_img = zeros(size(fil, 1), size(fil, 2));
%! vein_x_img = find_minima(true, fil, vein_x_img);
%! copy_cpp = cpp_vote(vein_x_img);
%! copy = vote(vein_x_img);
%! assert(copy, copy_cpp)
