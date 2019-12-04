package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func requiredFuel(mass int) int {
	// Part 1
	fuelReq := (mass / 3) - 2
	// Part 2
	if fuelReq <= 0 {
		return 0
	}
	return fuelReq + requiredFuel(fuelReq)
}

func main() {
	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var fuelReq int = 0

	scan := bufio.NewScanner(file)

	for scan.Scan() {
		mass, err := strconv.Atoi(scan.Text())
		if err != nil {
			log.Printf("Error converting line to int: %v", err)
		} else {
			fuelReq += requiredFuel(mass)
		}
	}
	fmt.Println(fuelReq)
}
