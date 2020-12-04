package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func readValues(fileName string) []int {
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	r := csv.NewReader(file)

	recordsMatrix, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	values := make([]int, len(recordsMatrix[0]))

	for i, value := range recordsMatrix[0] {
		values[i], err = strconv.Atoi(value)
		if err != nil {
			log.Printf("Error converting line to int: %v", err)
		}
	}

	return values
}

func restore1202(values []int) []int {
	restoredValues := append(values[:0:0], values...)

	restoredValues[1] = 12
	restoredValues[2] = 2

	return restoredValues
}

func findNounVerb(values []int) int {
	testValues := append(values[:0:0], values...)
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			testValues[1] = noun
			testValues[2] = verb
			output := runIntcode(testValues)
			if output == 19690720 {
				return 100*noun + verb
			}
		}
	}
	return -1
}

func runIntcode(values []int) int {
	processedValues := append(values[:0:0], values...)
loop:
	for i := 0; i < len(processedValues); i += 4 {
		num1 := processedValues[processedValues[i+1]]
		num2 := processedValues[processedValues[i+2]]
		pos := processedValues[i+3]

		switch processedValues[i] {
		case 1:
			processedValues[pos] = num1 + num2
		case 2:
			processedValues[pos] = num1 * num2
		case 99:
			break loop
		default:
			log.Printf("Error evaluating opcode %d\n", processedValues[i])
			return -1
		}
	}
	return processedValues[0]
}

func main() {
	values := readValues("./input")

	// Part 1
	restoredValues := restore1202(values)
	initialValue := runIntcode(restoredValues)
	fmt.Printf("Part 1: %d\n", initialValue)

	//Part 2
	nounVerb := findNounVerb(values)
	fmt.Printf("Part 2: %d\n", nounVerb)
}
