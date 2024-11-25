#include <stdio.h>

#define WIDTH 80     // Width of the output
#define HEIGHT 40    // Height of the output
#define MAX_ITER 100 // Maximum number of iterations

void draw_mandelbrot() {
  // Coordinates of the complex plane
  double xmin = -2.0, xmax = 1.0, ymin = -1.5, ymax = 1.5;

  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
      // Map pixel position to complex plane
      double real = xmin + (xmax - xmin) * x / (WIDTH - 1);
      double imag = ymin + (ymax - ymin) * y / (HEIGHT - 1);

      // Initialize z = 0
      double z_real = 0.0, z_imag = 0.0;
      int iter;

      // Mandelbrot iteration
      for (iter = 0; iter < MAX_ITER; iter++) {
        double z_real_sq = z_real * z_real;
        double z_imag_sq = z_imag * z_imag;

        if (z_real_sq + z_imag_sq > 4.0)
          break; // Diverges

        double z_new_real = z_real_sq - z_imag_sq + real;
        double z_new_imag = 2.0 * z_real * z_imag + imag;

        z_real = z_new_real;
        z_imag = z_new_imag;
      }

      // Choose a character based on the number of iterations
      char c = (iter == MAX_ITER) ? '#' : ' ';
      putchar(c);
    }
    putchar('\n'); // New line for next row
  }
}

int main() {
  draw_mandelbrot();
  return 0;
}

