package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type guard struct {
	timeCard [60]int
}

func printSchedule(guardsSchedule map[int]guard) {
	fmt.Print("ID\t")
	for i := 0; i < 60; i++ {
		fmt.Printf("%v ", i)
	}
	fmt.Print("\tSUM\n")
	for i, g := range guardsSchedule {
		sum := 0
		fmt.Printf("%v\t", i)
		for i, t := range g.timeCard {
			sum += t
			if i < 59 && i > 8 && g.timeCard[i+1] < 10 {
				fmt.Printf("%v  ", t)
			} else {
				fmt.Printf("%v ", t)
			}
		}
		fmt.Printf("\t%v\n", sum)
	}
}

func main() {
	var lines []string
	guardsSchedule := make(map[int]guard)

	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	for scan.Scan() {
		lines = append(lines, scan.Text())
	}

	sort.Strings(lines)

	currentGuardID := -1
	sleepTime := 0
	wakeTime := 0
	for _, line := range lines {
		if strings.Contains(line, "Guard") {
			currentGuardID, _ = strconv.Atoi(strings.Split(strings.Split(line, "#")[1], " ")[0])
			_, exists := guardsSchedule[currentGuardID]
			if !exists {
				guardsSchedule[currentGuardID] = *new(guard)
			}
		} else if strings.Contains(line, "falls asleep") {
			st, _ := strconv.Atoi(strings.Split(strings.Split(strings.Split(line, "]")[0], " ")[1], ":")[1])
			sleepTime = st
		} else if strings.Contains(line, "wakes up") {
			wt, _ := strconv.Atoi(strings.Split(strings.Split(strings.Split(line, "]")[0], " ")[1], ":")[1])
			wakeTime = wt
			timeSchedule := guardsSchedule[currentGuardID]
			for j := sleepTime; j < wakeTime; j++ {
				timeSchedule.timeCard[j]++
			}
			guardsSchedule[currentGuardID] = timeSchedule
		}
	}

	mostAsleepTime := -1
	mostAsleepID := -1
	for i, g := range guardsSchedule {
		sum := 0
		for _, t := range g.timeCard {
			sum += t
		}
		if sum > mostAsleepTime {
			mostAsleepTime = sum
			mostAsleepID = i
		}
	}

	mostAsleepMinute := -1
	max := -1
	for i, t := range guardsSchedule[mostAsleepID].timeCard {
		if t > max {
			max = t
			mostAsleepMinute = i
		}
	}
	fmt.Printf("Part One: %v\n", mostAsleepMinute*mostAsleepID)

	mostAsleepMinute = -1
	max = -1
	mostAsleepID = -1
	for i, g := range guardsSchedule {
		for j, t := range g.timeCard {
			if t > max {
				max = t
				mostAsleepMinute = j
				mostAsleepID = i
			}
		}
	}
	fmt.Printf("Part Two: %v\n", mostAsleepMinute*mostAsleepID)
}
