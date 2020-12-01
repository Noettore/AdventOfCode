package main

import (
	"bufio"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
	"sync"
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

func runIntcode(program []int, input <-chan int, output chan<- int, wg *sync.WaitGroup) {
	values := append([]int(nil), program...)
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
			values[paramAddress(1)] = <-input
			instructionPointer += 2

		case opcodeOutput:
			output <- values[paramAddress(1)]
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
	wg.Done()
}

func emulateAmplifiers(program []int, phases []int) int {
	var wg sync.WaitGroup

	fromEtoA := make(chan int, 1)
	fromAtoB := make(chan int)
	fromBtoC := make(chan int)
	fromCtoD := make(chan int)
	fromDtoE := make(chan int)

	fromAtoB <- phases[0]
	fromBtoC <- phases[1]
	fromCtoD <- phases[2]
	fromDtoE <- phases[3]
	fromEtoA <- phases[4]

	fromEtoA <- 0

	wg.Add(5)
	go runIntcode(program, fromEtoA, fromAtoB, &wg)
	go runIntcode(program, fromAtoB, fromBtoC, &wg)
	go runIntcode(program, fromBtoC, fromCtoD, &wg)
	go runIntcode(program, fromCtoD, fromDtoE, &wg)
	go runIntcode(program, fromDtoE, fromEtoA, &wg)

	fromAtoB <- phases[0]
	fromBtoC <- phases[1]
	fromCtoD <- phases[2]
	fromDtoE <- phases[3]
	fromEtoA <- phases[4]

	fromEtoA <- 0

	wg.Wait()

	return <-fromEtoA
}

func main() {
	//values := readValues("./input")
}
