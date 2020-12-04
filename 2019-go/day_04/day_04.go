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
	l := len(pwd)
	for i := 0; i < l-1; i++ {
		if pwd[i] == pwd[i+1] {
			return true
		}
	}
	return false
}

func twoExclusiveAdjacentDigits(pwd []int) bool {
	l := len(pwd)
	for i := 0; i < l-1; i++ {
		if pwd[i] == pwd[i+1] && (i == 0 || pwd[i] != pwd[i-1]) && (i == l-2 || pwd[i] != pwd[i+2]) {
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
	count1, count2 := 0, 0
	for i := min; i < max; i++ {
		pwd := intToSlice(i)
		two := twoEqualAdjacentDigits(pwd)
		onlyTwo := twoExclusiveAdjacentDigits(pwd)
		if increasingDigits(pwd) {
			if two {
				count1++
			}
			if onlyTwo {
				count2++
			}
		}
	}
	fmt.Printf("Part 1: %d\n", count1)
	fmt.Printf("Part 2: %d\n", count2)
}
