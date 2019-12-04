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

func wireTrace(cableMoves []string) mapset.Set {
	currentPosition := point{0, 0}
	cablePath := mapset.NewSet()
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
			cablePath.Add(currentPosition)
		}
	}
	return cablePath
}

func (p1 point) manhattanDistance(p2 point) int {
	return int(math.Abs(float64(p1.x-p2.x)) + math.Abs(float64(p1.y-p2.y)))
}

func main() {
	cablesMoves := readValues("./input")
	cable1Path := wireTrace(cablesMoves[0])
	cable2Path := wireTrace(cablesMoves[1])

	intersectionPoint := cable1Path.Intersect(cable2Path)
	if intersectionPoint.Cardinality() == 0 {
		log.Fatalln("No intersection point")
	}
	origin := point{0, 0}
	bestDistance := 0
	for p := range intersectionPoint.Iterator().C {
		dist := origin.manhattanDistance(p.(point))
		if bestDistance == 0 || dist < bestDistance {
			bestDistance = dist
		}
	}

	fmt.Printf("Part 1: %d\n", bestDistance)
}
