package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
)

type point struct {
	x  int
	y  int
	id int
}

type grid struct {
	points      [][]int
	coordinates []point
	currentID   int
	invalidIDs  map[int]bool
	maxX        int
	maxY        int
	minX        int
	minY        int
	maxArea     int
}

func (p1 point) manhattanDistance(p2 point) int {
	return int(math.Abs(float64(p1.x-p2.x)) + math.Abs(float64(p1.y-p2.y)))
}

func main() {
	var currentGrid grid

	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	for scan.Scan() {
		var p point

		line := scan.Text()
		fmt.Sscanf(line, "%d, %d", &p.x, &p.y)
		p.id = currentGrid.currentID
		currentGrid.currentID++

		currentGrid.coordinates = append(currentGrid.coordinates, p)

		if p.x > currentGrid.maxX {
			currentGrid.maxX = p.x
		}
		if p.y > currentGrid.maxY {
			currentGrid.maxY = p.y
		}
		if p.x < currentGrid.minX || currentGrid.minX == 0 {
			currentGrid.minX = p.x
		}
		if p.y < currentGrid.minY || currentGrid.minY == 0 {
			currentGrid.minY = p.y
		}
	}

	currentGrid.points = make([][]int, currentGrid.maxX)
	for i := range currentGrid.points {
		currentGrid.points[i] = make([]int, currentGrid.maxY)
	}

	for x := 0; x < currentGrid.maxX; x++ {
		for y := 0; y < currentGrid.maxY; y++ {
			minDist := -1
			minDistID := -1
			for i, c := range currentGrid.coordinates {
				dist := c.manhattanDistance(point{x: x, y: y})
				if i == 0 {
					minDist = dist
					minDistID = c.id
				} else if dist < minDist {
					minDist = dist
					minDistID = c.id
				} else if dist == minDist {
					minDistID = -1
				}
			}
			currentGrid.points[x][y] = minDistID
		}
	}

	currentGrid.invalidIDs = make(map[int]bool)
	for x := 0; x < currentGrid.maxX; x++ {
		currentGrid.invalidIDs[currentGrid.points[x][0]] = true
		currentGrid.invalidIDs[currentGrid.points[x][currentGrid.maxY-1]] = true
	}
	for y := 0; y < currentGrid.maxY; y++ {
		currentGrid.invalidIDs[currentGrid.points[0][y]] = true
		currentGrid.invalidIDs[currentGrid.points[currentGrid.maxX-1][y]] = true
	}

	for id := 0; id < currentGrid.currentID; id++ {
		count := 0
		for x := 0; x < currentGrid.maxX; x++ {
			for y := 0; y < currentGrid.maxY; y++ {
				if currentGrid.points[x][y] == id {
					count++
				}
			}
		}
		if count > currentGrid.maxArea {
			_, invalidID := currentGrid.invalidIDs[id]
			if !invalidID {
				currentGrid.maxArea = count
			}
		}
	}
	fmt.Printf("Part One: %v\n", currentGrid.maxArea)

	count := 0
	for x := 0; x < currentGrid.maxX; x++ {
		for y := 0; y < currentGrid.maxY; y++ {
			sum := 0
			for _, c := range currentGrid.coordinates {
				sum += c.manhattanDistance(point{x: x, y: y})
			}
			if sum < 10000 {
				count++
			}
		}
	}
	fmt.Printf("Part Two: %v\n", count)
}
