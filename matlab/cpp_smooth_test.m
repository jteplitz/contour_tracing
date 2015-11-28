% TODO: I took these tests straight from octave_smooth.m
% They kinda suck. We should write better ones
% In fact, we should get rid of this file and add tests in the cpp file that call octave_smooth and compare
% We also definitely need to test feature parity with even span values

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
%! ## random values
%! y = rand(500, 1);
%! yy = cpp_smooth(y, 9);
%! yy2 = octave_smooth(y, 9);
%! assert(yy, yy2, 1 * 10 ^-9);
