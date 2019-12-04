package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"

	mapset "github.com/deckarep/golang-set"
)

type point struct {
	x int
	y int
}

func readValues(fileName string) [][]string {
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	values := make([][]string, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lineElements := strings.Split(scanner.Text(), ",")
		values = append(values, lineElements)
	}
	return values
}

func wireTrace(cableMoves []string) ([]point, mapset.Set) {
	currentPosition := point{0, 0}
	cablePath := make([]point, 0)
	cableSet := mapset.NewSet()
	for _, step := range cableMoves {
		direction := step[0]
		distance, err := strconv.Atoi(string(step[1:]))
		if err != nil {
			log.Fatalf("Cannot decode step lenght: %c\n", step[1])
		}
		for i := 0; i < distance; i++ {
			switch direction {
			case 'U':
				currentPosition.y++
			case 'D':
				currentPosition.y--
			case 'R':
				currentPosition.x++
			case 'L':
				currentPosition.x--
			default:
				log.Fatalf("Cannot decode step direction: %c\n", direction)
			}
			cablePath = append(cablePath, currentPosition)
			cableSet.Add(currentPosition)
		}
	}
	return cablePath, cableSet
}

func (p1 point) manhattanDistance(p2 point) int {
	return int(math.Abs(float64(p1.x-p2.x)) + math.Abs(float64(p1.y-p2.y)))
}

func reachIntersect(cablePath []point, intersect point) int {
	for i, pos := range cablePath {
		if pos.x == intersect.x && pos.y == intersect.y {
			return i + 1
		}
	}
	return -1
}

func shortestDistance(intersectionPoints mapset.Set) int {
	origin := point{0, 0}
	bestDistance := 0
	for p := range intersectionPoints.Iterator().C {
		dist := origin.manhattanDistance(p.(point))
		if bestDistance == 0 || dist < bestDistance {
			bestDistance = dist
		}
	}
	return bestDistance
}

func fewestSteps(cablesPath [][]point, intersectionPoints mapset.Set) int {
	bestSteps := 0
	for p := range intersectionPoints.Iterator().C {
		steps := reachIntersect(cablesPath[0], p.(point)) + reachIntersect(cablesPath[1], p.(point))
		if bestSteps == 0 || steps < bestSteps {
			bestSteps = steps
		}
	}
	return bestSteps
}

func main() {
	cablesMoves := readValues("./input")
	cable1Path, cable1Set := wireTrace(cablesMoves[0])
	cable2Path, cable2Set := wireTrace(cablesMoves[1])

	intersectionPoints := cable1Set.Intersect(cable2Set)
	if intersectionPoints.Cardinality() == 0 {
		log.Fatalln("No intersection point")
	}

	// Part 1
	dist := shortestDistance(intersectionPoints)
	fmt.Printf("Part 1: %d\n", dist)

	//Part 2
	steps := fewestSteps([][]point{cable1Path, cable2Path}, intersectionPoints)
	fmt.Printf("Part 2: %d\n", steps)
}
