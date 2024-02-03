package mouse

import (
	"math"
	"math/rand"
)

func interpolate[T float32 | float64](x, y, t T) T {
	return y*t + x*(1-t)
}

// createGaussian creates a gaussian function with the given mean and standard deviation.
//
// This function uses the Marsaglia polar method. Read more:
//
// https://en.wikipedia.org/wiki/Marsaglia_polar_method
func createGaussian(mean, stdev float64) func() float64 {
	var y2 float64
	useLast := false

	return func() float64 {
		var y1 float64
		if useLast {
			y1 = y2
			useLast = false
		} else {
			var x1, x2, w float64

			for ok := true; ok; ok = w >= 1 {
				x1 = 2*rand.Float64() - 1
				x2 = 2*rand.Float64() - 1
				w = x1*x1 + x2*x2
			}

			w = math.Sqrt((-2 * math.Log(w)) / w)
			y1 = x1 * w
			y2 = x2 * w
			useLast = true
		}

		return mean + (stdev * y1)
	}
}
