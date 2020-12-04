package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
)

type graph map[string][]string

type task struct {
	time int
	task string
}

func popMinimumTask(tasks []task) (int, string, []task) {
	var minTime = 2147483647
	var minTasks = make([]task, 0)
	for _, t := range tasks {
		if t.time < minTime {
			minTasks = []task{t}
			minTime = t.time
		} else if t.time == minTime {
			minTasks = append(minTasks, t)
		}
	}

	var minTask task
	var minID = string("Z")

	for _, t := range minTasks {
		if t.task <= minID {
			minID = t.task
			minTask = t
		}
	}

	var removed = make([]task, 0)
	for _, val := range tasks {
		if !(val.task == minTask.task && val.time == minTask.time) {
			removed = append(removed, val)
		}
	}

	return minTask.time, minTask.task, removed
}

func popMinimumString(strs []string) (string, []string) {
	if len(strs) == 0 {
		return "", nil
	}
	min := strs[0]
	for _, str := range strs {
		if str < min {
			min = str
		}
	}
	var removed = make([]string, 0)
	for _, str := range strs {
		if str != min {
			removed = append(removed, str)
		}
	}
	return min, removed
}

func main() {

	var gr = make(graph)
	var incoming = make(map[string]int)
	var incomingSaved = make(map[string]int) // for Part 2

	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		var start, end string
		fmt.Sscanf(line, "Step %s must be finished before step %s can begin.", &start, &end)

		if _, ok := gr[start]; ok {
			gr[start] = append(gr[start], end)
		} else {
			gr[start] = []string{end}
		}

		if _, ok := incoming[end]; ok {
			incoming[end]++
			incomingSaved[end]++
		} else {
			incoming[end] = 1
			incomingSaved[end] = 1
		}
	}

	var queue, taskQueue = make([]string, 0), make([]string, 0)

	for key, value := range gr {
		sort.Strings(value)
		gr[key] = value
		if incoming[key] == 0 {
			queue = append(queue, key)
		}
	}

	taskQueue = append(taskQueue, queue...)

	var result string
	for len(queue) != 0 {
		sort.Strings(queue)
		init := queue[0]
		var temp []string
		for _, v := range queue {
			if v != init {
				temp = append(temp, v)
			}
		}
		queue = temp
		result += init
		for _, key := range gr[init] {
			incoming[key]--
			if incoming[key] == 0 {
				queue = append(queue, key)
			}
		}
	}

	fmt.Printf("Part 1: %s\n", result)

	// Part 2
	var currentTime int
	var currentTask string
	var tasks = make([]task, 0)

	for len(tasks) < 5 && len(taskQueue) > 0 {
		var next string
		if nxt, q := popMinimumString(taskQueue); q != nil {
			next = nxt
			taskQueue = q
			tasks = append(tasks, task{time: currentTime + int([]byte(next)[0]) - 4, task: next})
		}
	}

	for len(tasks) > 0 || len(taskQueue) > 0 {
		currentTime, currentTask, tasks = popMinimumTask(tasks)
		for _, key := range gr[currentTask] {
			incomingSaved[key]--
			if incomingSaved[key] == 0 {
				taskQueue = append(taskQueue, key)
			}
		}
		for len(tasks) < 5 && len(taskQueue) > 0 {
			var next string
			if nxt, q := popMinimumString(taskQueue); q != nil {
				next = nxt
				taskQueue = q
				tasks = append(tasks, task{time: currentTime + int([]byte(next)[0]) - 4, task: next})
			}
		}
	}

	fmt.Printf("Part 2: %v\n", currentTime)
}
