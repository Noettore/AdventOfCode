package main

import (
	"fmt"
	"math"
)

const gridSize int = 300
const gridSerial int = 7347

func cellPower(x int, y int, serial int) int {
	rackID := x + 1 + 10
	powerLevel := rackID * (y + 1)
	powerLevel += serial
	powerLevel *= rackID
	powerLevel %= int(math.Pow(10, 3))
	powerLevel /= int(math.Pow(10, 2))

	return powerLevel
}

func maxPowerSquare(powerGrid *[gridSize][gridSize]int, powerGridCheck *[gridSize][gridSize]bool, size int, res chan<- [4]int) {
	maxSum := 0
	maxSumCheck := false
	maxX, maxY := 0, 0

	for x := 0; x < gridSize-size+1; x++ {
		for y := 0; y < gridSize-size+1; y++ {
			powerSum := 0
			for xi := x; xi < x+size; xi++ {
				for yi := y; yi < y+size; yi++ {
					if !powerGridCheck[xi][yi] {
						powerGrid[xi][yi] = cellPower(xi, yi, gridSerial)
						powerGridCheck[xi][yi] = true
					}
					powerSum += powerGrid[xi][yi]
				}
			}
			if powerSum > maxSum || !maxSumCheck {
				maxSum = powerSum
				maxSumCheck = true
				maxX = x
				maxY = y
			}
		}
	}
	res <- [4]int{size, maxSum, maxX + 1, maxY + 1}
}

func main() {

	var powerGrid [gridSize][gridSize]int
	var powerGridCheck [gridSize][gridSize]bool
	var res = make(chan [4]int)

	go func() {
		maxPowerSquare(&powerGrid, &powerGridCheck, 3, res)
		close(res)
	}()
	p1 := <-res
	fmt.Printf("Part One: %v,%v\n", p1[2], p1[3])

	res = make(chan [4]int)
	for i := 0; i < gridSize; i++ {
		go func(i int) {
			maxPowerSquare(&powerGrid, &powerGridCheck, i, res)
			if i == gridSize-1 {
				close(res)
			}
		}(i)
	}

	maxSum := 0
	maxSumCheck := false
	maxX, maxY := 0, 0
	maxSize := 0

	for r := range res {
		fmt.Printf("Size: %v\t Sum: %v\t x: %v\t y: %v\n", r[0], r[1], r[2], r[3])
		if r[1] > maxSum || !maxSumCheck {
			maxSize = r[0]
			maxSum = r[1]
			maxSumCheck = true
			maxX = r[2]
			maxY = r[3]
		}
	}
	fmt.Printf("Part Two: %v,%v,%v\n", maxX, maxY, maxSize)

	res = make(chan [4]int)
	go func() {
		maxPowerSquare(&powerGrid, &powerGridCheck, 299, res)
		close(res)
	}()
	p1 = <-res
	fmt.Printf("Part Two 299: %v,%v,%v\n", p1[1], p1[2], p1[3])

}
