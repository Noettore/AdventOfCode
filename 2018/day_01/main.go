package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	//count to maintain the total sum of the frequence changes
	count := 0
	//current to maintain the partial frequence at a stage
	current := 0
	//freqChange to store the individual frequence changes
	var freqChange []int
	//freqList to store all the stage frequences
	freqList := map[int]bool{0: true}

	//We open the input file
	file, err := os.Open("./input")
	if err != nil {
		//If there is an error we print it in the stderr and exit(1)
		log.Fatal(err)
	}
	//We defer the closure of the file
	defer file.Close()

	//We create a scanner to the file
	scan := bufio.NewScanner(file)

	//We iterate throught the file line
	for scan.Scan() {
		//We convert each line into an int
		num, err := strconv.Atoi(scan.Text())
		if err != nil {
			//If the conversion generate an error we print it to stderr
			log.Printf("Error converting line to int: %v", err)
		} else {
			//Otherwise we add the current freq change to count
			count += num
			//And we append it to freqChange
			freqChange = append(freqChange, num)
		}
	}

	fmt.Printf("Part One: %v\n", count)

	for {
		for _, freqMod := range freqChange {
			current += freqMod
			_, found := freqList[current]
			if found {
				fmt.Printf("Part Two: %v\n", current)
				os.Exit(0)
			} else {
				freqList[current] = true
			}
		}
	}
}
