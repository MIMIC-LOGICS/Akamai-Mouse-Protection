package mouse

import (
	"math/rand"
	"strings"
	"testing"
	"math"
)


import (
	"strconv"
)

func TestGenRandom(t *testing.T) {
	var builder strings.Builder
	var size = 100
	var cycles = 3
	var multiplier = 2

	const (
		min float64 = 0
		max float64 = 1000
	)

	randoms := make([]float64, 2+int(math.Ceil(float64((size-1)/(size/int(math.Pow(2, float64(cycles))))))))
	for j := 0; j < len(randoms); j++ {
		randoms[j] = min + rand.Float64()*(max/float64(multiplier))
		// convert random to string
		str := strconv.FormatFloat(randoms[j], 'f', -1, 64)
		builder.WriteString(str + ",")
	}

	t.Log(builder.String())
}


func TestGenLine(t *testing.T) {
	var builder strings.Builder
	var size = 100
	var cycles = 3
	var multiplier = 2
	var smoothing = 0.955

	const (
		min float64 = 0
		max float64 = 1000
	)
	var result = make([]float64, size)
	for i := 0; i < cycles; i++ {

		randoms := make([]float64, 2+int(math.Ceil(float64((size-1)/(size/int(math.Pow(2, float64(cycles))))))))
		for j := 0; j < len(randoms); j++ {
			randoms[j] = min + rand.Float64()*(max/float64(multiplier))
		}
		segmentSize := math.Floor(float64(size / multiplier))
		for j := 0; j < size; j++ {
			currentSegment := math.Floor(float64(j) / segmentSize)
			//builder.WriteString(str + ",")

			
			ratio := float64(j)/segmentSize - math.Floor(float64(j)/segmentSize)
			result[j] += interpolate(randoms[int(currentSegment)], randoms[int(currentSegment)+1], ratio)

			// convert result to string
			str := strconv.FormatFloat(result[j], 'f', -1, 64)
			builder.WriteString(str + ",")
		}
		builder.WriteString("\n")
		builder.WriteString("\n")

		multiplier *= 2

	}
	var result1 = make([]float64, len(result))

	result1[0] = result[0]
	for i := 1; i < len(result); i++ {
		result1[i] = (1-smoothing)*result[i] + smoothing*result1[i-1]
		str := strconv.FormatFloat(result1[i], 'f', -1, 64)
		builder.WriteString(str + ",")
	}


	t.Log(builder.String())
}