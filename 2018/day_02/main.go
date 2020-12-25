package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func checkDuplicates(s string) (bool, bool) {
	two := false
	three := false
	charsInString := map[string]int{}
	chars := strings.Split(s, "")
	for _, c := range chars {
		charsInString[c]++
	}
	for _, c := range charsInString {
		if c == 2 {
			two = true
		} else if c == 3 {
			three = true
		}
	}
	return two, three
}

func compareStrings(s1, s2 string) (string, bool) {
	diffCount := 0
	diffString := ""
	for i := 0; i < len(s1) && diffCount < 2; i++ {
		if s1[i] == s2[i] {
			diffString += string(s1[i])
		} else {
			diffCount++
		}
	}
	if diffCount >= 2 {
		return "", false
	}
	return diffString, true
}

func main() {
	twos := 0
	threes := 0
	var stringStore []string
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
		currentString := scan.Text()
		stringStore = append(stringStore, currentString)
		two, three := checkDuplicates(currentString)
		if two {
			twos++
		}
		if three {
			threes++
		}
	}
	fmt.Printf("Part One: the checksum is %v\n", twos*threes)

	for i, str := range stringStore {
		for j := i + 1; j < len(stringStore); j++ {
			ret, valid := compareStrings(str, stringStore[j])
			if valid {
				fmt.Printf("Part Two: the common letters are %v\n", ret)
				os.Exit(0)
			}
		}
	}
}
