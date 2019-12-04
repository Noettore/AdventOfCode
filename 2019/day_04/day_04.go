package main

import "fmt"

const (
	min = 130254
	max = 678275
)

func intToSlice(n int) []int {
	s := make([]int, 0)
	for n != 0 {
		r := n % 10
		n = n / 10
		s = append([]int{r}, s...)
	}
	return s
}

func twoEqualAdjacentDigits(pwd []int) bool {
	for i, digit := range pwd {
		if i < len(pwd)-1 && digit == pwd[i+1] {
			return true
		}
	}
	return false
}

func increasingDigits(pwd []int) bool {
	for i, digit := range pwd {
		if i < len(pwd)-1 && digit > pwd[i+1] {
			return false
		}
	}
	return true
}

func main() {
	// Part 1:
	count := 0
	for i := min; i < max; i++ {
		pwd := intToSlice(i)
		if twoEqualAdjacentDigits(pwd) && increasingDigits(pwd) {
			count++
		}
	}
	fmt.Printf("Part 1: %d\n", count)
}
