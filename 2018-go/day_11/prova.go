package main

import (
	"fmt"
	"strconv"
)

func calculate(i int, j int, memo *[][]int, ps *[][]int, input int) int {
	t := 0
	for x := i; x < i+3; x++ {
		for y := j; y < j+3; y++ {
			if (*memo)[y][x] != 0 {
				t += (*memo)[y][x]
			} else {
				id := x + 10
				serial := (id*y + input)
				hundreds := strconv.Itoa(serial * id)
				var result int
				if len(hundreds) >= 3 {
					result, _ = strconv.Atoi(string(hundreds[len(hundreds)-3]))
				}
				result -= 5
				t += result
				(*memo)[y][x] = result
				(*ps)[y][x] = result + (*ps)[y-1][x] + (*ps)[y][x-1] - (*ps)[y-1][x-1]
			}
		}
	}
	return t
}

func main() {

	input := 7347

	var res, X, Y int

	// technically memo isn't needed anymore but I added partial sums after
	// part 2 and didn't wanna clean up my code after for part 1
	memo := make([][]int, 301)
	partialSums := make([][]int, 301)
	for i := range memo {
		memo[i] = make([]int, 301)
		partialSums[i] = make([]int, 301)
	}

	for i := 1; i <= 298; i++ {
		for j := 1; j <= 298; j++ {
			if c := calculate(i, j, &memo, &partialSums, input); c > res {
				res = c
				X = i
				Y = j
			}
		}
	}

	fmt.Printf("Part 1: %v, %v, %v\n", res, X, Y)

	res = 0
	var sz int

	for size := 1; size < 300; size++ {
		for i := size; i <= 300; i++ {
			for j := size; j <= 300; j++ {
				if c := partialSums[i][j] - partialSums[i-size][j] -
					partialSums[i][j-size] + partialSums[i-size][j-size]; c > res {
					res = c
					Y = i - size + 1
					X = j - size + 1
					sz = size
				}
			}
		}
	}

	fmt.Printf("Part 2: %v, %v, %v, %v\n", res, X, Y, sz)
}
