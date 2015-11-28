#include <octave/oct.h>

int countNeighbors(Matrix &vein_x_img, size_t row, size_t col);

DEFUN_DLD (cpp_vote, args, nargout, "C++ Vote") {
  int nargin = args.length();

  if (nargin != 1) {
    print_usage();
    // TODO: Figure out how to throw an error
    return octave_value_list ();
  } else {
    Matrix vein_x_img = args(0).matrix_value();
    Matrix copy(vein_x_img);

    for (size_t i = 1; i < vein_x_img.rows() - 1; i++){
      for (size_t j = 1; j < vein_x_img.cols() - 1; j++) {
        int numNeighbors = countNeighbors(vein_x_img, i, j);
        if (numNeighbors > 1) {
          vein_x_img(i, j) = 1;
        } else {
          vein_x_img(i, j) = 0;
        }
      }
    }

    return octave_value(copy);
  }
}

/**
 * Returns the number of neighboring minima to this pixel
 * Includes the given pixel in the count
 */
int countNeighbors(Matrix &vein_x_img, size_t row, size_t col) {
  int numNeighbors = 0;
  for (size_t i = row - 1; i <= row + 1; i++) {
    for (size_t j = col - 1; j <= col + 1; j++) {
      numNeighbors += vein_x_img(i, j);
    }
  }

  return numNeighbors;
}
