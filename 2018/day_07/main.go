package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

type step struct {
	ID   string
	time int
	next []*step
	prev []*step
}

func alreadyExecuted(executed []string, steps []*step) bool {
	for _, s := range steps {
		found := false
		for _, e := range executed {
			if e == s.ID {
				found = true
			}
		}
		if !found {
			return false
		}
	}
	return true
}

func alreadyInQueue(queue []string, s *step) bool {
	for _, q := range queue {
		if s.ID == q {
			return true
		}
	}
	return false
}

func main() {
	var queue []string
	var executionOrder []string
	stepAddr := make(map[string]*step)

	file, err := os.Open("./input_less")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	for scan.Scan() {
		line := scan.Text()

		splittedLine := strings.Split(line, " ")
		currentID := splittedLine[1]
		nextID := splittedLine[7]

		currentStep, csExists := stepAddr[currentID]
		nextStep, nsExists := stepAddr[nextID]

		if !csExists {
			cs := step{ID: currentID, time: int(currentID[0]) - 64}
			stepAddr[currentID] = &cs
			currentStep = &cs
		}
		if !nsExists {
			ns := step{ID: nextID, time: int(nextID[0]) - 64}
			stepAddr[nextID] = &ns
			nextStep = &ns
		}

		currentStep.next = append(currentStep.next, nextStep)
		nextStep.prev = append(nextStep.prev, currentStep)
	}

	for _, s := range stepAddr {
		if len(s.prev) == 0 {
			queue = append(queue, s.ID)
		}
	}
	sort.Strings(queue)
	i := 0
	for i < len(queue) {
		sPrev := stepAddr[queue[i]].prev
		if len(sPrev) == 0 || alreadyExecuted(executionOrder, sPrev) {
			executionOrder = append(executionOrder, queue[i])
			for _, n := range stepAddr[queue[i]].next {
				if !alreadyInQueue(queue, n) {
					queue = append(queue, n.ID)
				}
			}

			queue = append(queue[:i], queue[i+1:]...)

			sort.Strings(queue)
			i = 0
		} else {
			i++
		}
	}

	fmt.Printf("Part One: %v\n", strings.Join(executionOrder, ""))

	for _, s := range stepAddr {
		if len(s.prev) == 0 {
			queue = append(queue, s.ID)
			fmt.Printf("Added in queue: %v\n", s.ID)
		}
	}
	sort.Strings(queue)

	currentTime := 0
	var times [2]int
	var workers [2]string
	var availableSteps []*step
	working := false
	executionOrder = make([]string, 0)
	for len(queue) > 0 || len(availableSteps) > 0 || working {
		if len(queue) > 0 {
			for i := 0; i < len(queue); i++ {
				fmt.Printf("Analyzing from queue step %v\t i:%v\n", queue[i], i)
				sPrev := stepAddr[queue[i]].prev
				if len(sPrev) == 0 || alreadyExecuted(executionOrder, sPrev) {
					availableSteps = append(availableSteps, stepAddr[queue[i]])
					for _, n := range stepAddr[queue[i]].next {
						if !alreadyInQueue(queue, n) {
							queue = append(queue, n.ID)
							fmt.Printf("Added in queue: %v\n", n.ID)
						}
					}
					fmt.Printf("Added to availableSteps: %v\n", queue[i])
					fmt.Printf("Removed from queue: %v\n", queue[i])
					queue = append(queue[:i], queue[i+1:]...)
					i = -1
				}
			}
		}
		sort.Slice(availableSteps, func(i, j int) bool {
			return availableSteps[i].ID < availableSteps[j].ID
		})
		if len(availableSteps) > 0 || working {
			for w := 0; w < len(workers); w++ {
				if workers[w] == "" && len(availableSteps) > 0 {
					workers[w] = availableSteps[0].ID
					times[w] = availableSteps[0].time
					working = true
					fmt.Printf("Assigned to worker %v step %v\n", w, availableSteps[0].ID)
					fmt.Printf("Removed from availableSteps: %v\n", availableSteps[0].ID)
					availableSteps = availableSteps[1:]
				} else if workers[w] != "" {
					times[w]--
					fmt.Printf("Decreased time of worker %v to %v\n", w, times[w])
					if times[w] == 0 {
						executionOrder = append(executionOrder, workers[w])
						fmt.Printf("Worker %v has completed step %v\n", w, workers[w])
						workers[w] = ""
						times[w] = 0
						//if times[0]+times[1]+times[2]+times[3]+times[4] == 0 {
						if times[0]+times[1] == 0 {
							working = false
						}
					}
				}
			}
			if working {
				currentTime++
				fmt.Printf("Increaset currentTime to %v\n", currentTime)
			}
		}
	}
	fmt.Printf("Part Two: %v\t%v\n", currentTime, executionOrder)
}
