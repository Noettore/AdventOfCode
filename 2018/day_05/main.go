package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

var alphabet string

func react(s string) string {
	firstS := s
	for i := 0; i < len(alphabet); i++ {
		letter := alphabet[i : i+1]
		s = strings.Replace(s, letter+strings.ToUpper(letter), "", -1)
		s = strings.Replace(s, strings.ToUpper(letter)+letter, "", -1)
	}
	if firstS == s {
		return s
	} else {
		return react(s)
	}

}

func main() {
	var input string
	alphabet = "abcdefghijklmnopqrstuvwxyz"

	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	for scan.Scan() {
		input = scan.Text()
	}
	fmt.Printf("Part One: %v\n", len(react(input)))

	min := len(input)
	for i := 0; i < len(alphabet); i++ {
		letter := alphabet[i : i+1]
		try := input
		try = strings.Replace(try, letter, "", -1)
		try = strings.Replace(try, strings.ToUpper(letter), "", -1)
		size := len(react(try))
		if size < min {
			min = size
		}
	}
	fmt.Printf("Part Two: %v\n", min)
}
