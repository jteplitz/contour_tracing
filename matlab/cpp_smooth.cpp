#include <octave/oct.h>

double mean(ColumnVector &vec, int start, int end);

DEFUN_DLD (cpp_smooth, args, nargout, "C++ Smooth") {
  int nargin = args.length ();

  if (nargin != 2) {
    print_usage();
    // TODO: Figure out how to throw an error
    return octave_value_list ();
  } else {
    ColumnVector m = args(0).vector_value();
    int windowSize = args(1).int_value();
    ColumnVector out(m.nelem());

    out(0) = 5;

    for (int i = 0; i < m.nelem(); i++){
      // for now just do full mean calculation for the edges
      // can replace with something smarter later if we want but I don't think it'll matter
      if (i <= (windowSize - 1) / 2) {
        // beginning of vector, use smaller window to keep i centered
        out(i) = mean(m, 0, 2 * i);
      } else if (i < m.nelem() - (windowSize - 1) / 2) {
        // middle of vector
        int offset = (windowSize - 1) / 2;
        out(i) = out(i - 1) - (m(i - offset - 1) - m(i + offset)) / windowSize;
      } else {
        // end of vector
        int offset = m.nelem() - i - 1;
        out(i) = mean(m, i - offset, i + offset);
      }
    }

    return octave_value(out.as_row());
  }
}

double mean(ColumnVector &vec, int start, int end) {
  double sum = 0;
  for (int i = start; i <= end; i++) {
    sum += vec(i);
  }
  return sum / (end - start + 1);
}
