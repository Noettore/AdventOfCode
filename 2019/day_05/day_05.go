package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	opcodeAdd         = 1
	opcodeMultiply    = 2
	opcodeInput       = 3
	opcodeOutput      = 4
	opcodeJumpIfTrue  = 5
	opcodeJumpIfFalse = 6
	opcodeLessThan    = 7
	opcodeEquals      = 8
	opcodeHalt        = 99

	paramModePosition  = 0
	paramModeImmediate = 1
)

func readValues(fileName string) []int {
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var values []int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lineElements := strings.Split(scanner.Text(), ",")
		for _, elem := range lineElements {
			n, err := strconv.Atoi(elem)
			if err != nil {
				log.Fatalf("Cannot convert to int: %s\n", elem)
			}
			values = append(values, n)
		}
	}
	return values
}

func runIntcode(values []int) {
	instructionPointer := 0
	for values[instructionPointer] != opcodeHalt {
		instruction := values[instructionPointer]
		opCode := instruction % 100

		paramAddress := func(n int) int {
			mode := (instruction % int(math.Pow10(n+2))) / int(math.Pow10(n+1))
			switch mode {
			case paramModeImmediate:
				return instructionPointer + n
			default:
				return values[instructionPointer+n]
			}
		}

		switch opCode {
		case opcodeInput:
			var input int
			fmt.Print("Input: ")
			_, err := fmt.Scanf("%d", &input)
			if err != nil {
				log.Fatalf("Cannot read integer from stdin: %s", err)
			}
			values[paramAddress(1)] = input
			instructionPointer += 2
		case opcodeOutput:
			fmt.Printf("Output: %d\n", values[paramAddress(1)])
			instructionPointer += 2
		case opcodeAdd:
			values[paramAddress(3)] = values[paramAddress(1)] + values[paramAddress(2)]
			instructionPointer += 4
		case opcodeMultiply:
			values[paramAddress(3)] = values[paramAddress(1)] * values[paramAddress(2)]
			instructionPointer += 4
		case opcodeJumpIfTrue:
			if values[paramAddress(1)] != 0 {
				instructionPointer = values[paramAddress(2)]
			} else {
				instructionPointer += 3
			}
		case opcodeJumpIfFalse:
			if values[paramAddress(1)] == 0 {
				instructionPointer = values[paramAddress(2)]
			} else {
				instructionPointer += 3
			}
		case opcodeLessThan:
			if values[paramAddress(1)] < values[paramAddress(2)] {
				values[paramAddress(3)] = 1
			} else {
				values[paramAddress(3)] = 0
			}
			instructionPointer += 4
		case opcodeEquals:
			if values[paramAddress(1)] == values[paramAddress(2)] {
				values[paramAddress(3)] = 1
			} else {
				values[paramAddress(3)] = 0
			}
			instructionPointer += 4
		default:
			log.Fatalf("Unknown opCode: %d\n", opCode)
		}
	}
}

func main() {
	values := readValues("./input")
	runIntcode(values)
}
