package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func readValues(fileName string) map[string]string {
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	orbits := make(map[string]string)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		value := scanner.Text()
		planets := strings.Split(value, ")")
		orbits[planets[1]] = planets[0]
	}

	return orbits
}

func getOrbitsNum(planet string, orbits map[string]string) int {
	orbitsNum := 0
	key := planet
	orbit, hasOrbit := orbits[key]

	for hasOrbit {
		orbitsNum++
		key = orbit
		orbit, hasOrbit = orbits[key]
	}

	return orbitsNum
}

func getMinOrbitalTransfers(from string, to string, orbits map[string]string) int {
	path := make(map[string]int)
	orbit, hasOrbit := orbits[from]
	distance := 0

	for hasOrbit {
		distance++
		path[orbit] = distance
		orbit, hasOrbit = orbits[orbit]
	}

	orbit, hasOrbit = orbits[to]
	distance = 0

	for hasOrbit {
		dist, isInPath := path[orbit]
		if isInPath {
			distance += dist
			return distance - 1
		}
		distance++
		orbit, hasOrbit = orbits[orbit]
	}
	return -1
}

func main() {
	orbits := readValues("./input")

	orbitsNum := 0
	for planet := range orbits {
		orbitsNum += getOrbitsNum(planet, orbits)
	}
	fmt.Printf("Part 1: %d\n", orbitsNum)

	minDist := getMinOrbitalTransfers("YOU", "SAN", orbits)
	fmt.Printf("Part 2: %d\n", minDist)
}
