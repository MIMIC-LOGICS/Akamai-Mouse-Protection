package mouse

import (
	"math"
	"math/rand"
)

// GenerateEvents generates mouse events given the number of events to generate.
// The inner width and height are used as a max boundary for X and Y coordinates.
func GenerateEvents(n, innerWidth, innerHeight int) (movements [][2]float64, delays []int64) {
	const (
		cycles    = 3
		smoothing = 0.955
	)

	arrX := smooth(generateLine(n, cycles), smoothing)
	minX, maxX := getLimitsX(float64(innerWidth))
	arrX = rescale(arrX, minX, maxX)

	arrY := smooth(generateLine(n, cycles), smoothing)
	minY, maxY := getLimitsY(float64(innerHeight))
	arrY = rescale(arrY, minY, maxY)

	movements = make([][2]float64, n)
	delays = generateDelays(n)
	for i := 0; i < n; i++ {
		movements[i] = [2]float64{arrX[i], arrY[i]}
	}
	return
}

func getLimitsX(innerWidth float64) (float64, float64) {
	const margin = 0.2
	randomXMin := createGaussian(innerWidth*margin, innerWidth*margin)
	randomXDiff := createGaussian(innerWidth*(1-2*margin), innerWidth*margin)

	min := randomXMin()
	for min < 0 || min > 3*innerWidth*margin {
		min = randomXMin()
	}

	diff := randomXDiff()
	for diff < innerWidth*(1-3*margin) || diff > innerWidth {
		diff = randomXDiff()
	}

	return min, min + diff
}

func getLimitsY(innerHeight float64) (float64, float64) {
	const margin = 0.2
	randomYMin := createGaussian(innerHeight*margin, innerHeight*margin)
	randomYDiff := createGaussian(innerHeight*(1-2*margin), innerHeight*margin)

	min := randomYMin()
	for min < 0 || min > 3*innerHeight*margin {
		min = randomYMin()
	}

	diff := randomYDiff()
	for diff < innerHeight*(1-3*margin) || diff > innerHeight {
		diff = randomYDiff()
	}

	return min, min + diff
}

func generateLine(size, cycles int) (result []float64) {
	const (
		min float64 = 0
		max float64 = 1000
	)

	result = make([]float64, size)
	for i := 0; i < size; i++ {
		result[i] = min
	}

	multiplier := 2
	for i := 0; i < cycles; i++ {
		randoms := make([]float64, 2+int(math.Ceil(float64((size-1)/(size/int(math.Pow(2, float64(cycles))))))))
		for j := 0; j < len(randoms); j++ {
			randoms[j] = min + rand.Float64()*(max/float64(multiplier))
		}

		segmentSize := math.Floor(float64(size / multiplier))
		for j := 0; j < size; j++ {
			currentSegment := math.Floor(float64(j) / segmentSize)
			
			ratio := float64(j)/segmentSize - math.Floor(float64(j)/segmentSize)
			result[j] += interpolate(randoms[int(currentSegment)], randoms[int(currentSegment)+1], ratio)
		}
		multiplier *= 2
	}
	
	return
}

func smooth(arr []float64, smoothing float64) (result []float64) {
	result = make([]float64, len(arr))
	result[0] = arr[0]
	for i := 1; i < len(arr); i++ {
		
		result[i] = (1-smoothing)*arr[i] + smoothing*result[i-1]
	}
	return
}

func rescale(arr []float64, min, max float64) (result []float64) {
	result = make([]float64, len(arr))
	oldMin, oldMax := arr[0], arr[1]
	for i := 0; i < len(arr); i++ {
		if oldMin > arr[i] {
			oldMin = arr[i]
		}

		if oldMax < arr[i] {
			oldMax = arr[i]
		}
	}

	for i := 0; i < len(arr); i++ {
		result[i] = ((arr[i]-oldMin)/(oldMax-oldMin))*(max-min) + min
	}
	return
}

func generateDelays(n int) (result []int64) {
	result = make([]int64, n)
	randomStep := createGaussian(7.9, 0.47)

	for i := 0; i < n; i++ {
		t := randomStep()
		for t < 4 || t > 11.8 {
			t = randomStep()
		}
		result[i] = int64(t + math.Copysign(0.5, t))
	}

	return
}
