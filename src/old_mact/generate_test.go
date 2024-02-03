package mouse

import (
	"math/rand"
	"strconv"
	"strings"
	"testing"
	"log"
	"bytes"
	"fmt"
)

func TestGenerateEvents(t *testing.T) {
	var builder strings.Builder
	var buf bytes.Buffer
    logger := log.New(&buf, "logger: ", log.Lshortfile)

	const n = 100
	movements, delays := GenerateEvents(n, 1920, 1800)
	var currentTime int64
	for i := 0; i < n; i++ {
		builder.WriteString(strconv.Itoa(i))
		builder.WriteString(",1,")
		builder.WriteString(strconv.FormatInt(currentTime, 10))
		builder.WriteString(",")
		builder.WriteString(strconv.Itoa(int(movements[i][0])))
		builder.WriteString(",")
		builder.WriteString(strconv.Itoa(int(movements[i][1])))
		builder.WriteString(";")

		currentTime += delays[i]
	}

	logger.Println(builder.String())

    // At the end of the test, print the buffer's contents
    fmt.Println(buf.String())}

func BenchmarkGenerateEvents(b *testing.B) {
	rand.Seed(165527284833122202)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		GenerateEvents(100, 1920, 1080)
	}
}
