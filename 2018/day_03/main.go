package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type claim struct {
	x           int
	y           int
	len         int
	height      int
	overlapping bool
}

func main() {
	var fabric [1000][1000]int
	claims := make(map[int]*claim)
	inchesCount := 0
	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)

	for scan.Scan() {
		line := scan.Text()
		line = strings.Join(strings.Fields(line), "")

		info := strings.Split(line, "#")[1]
		id, _ := strconv.Atoi(strings.Split(info, "@")[0])
		measures := strings.Split(info, "@")[1]
		xy := strings.Split(strings.Split(measures, ":")[0], ",")
		dim := strings.Split(strings.Split(measures, ":")[1], "x")
		x, _ := strconv.Atoi(xy[0])
		y, _ := strconv.Atoi(xy[1])
		len, _ := strconv.Atoi(dim[0])
		height, _ := strconv.Atoi(dim[1])

		newClaim := claim{x, y, len, height, false}

		for i := x; i < x+len; i++ {
			for j := y; j < y+height; j++ {
				if fabric[i][j] == 0 {
					fabric[i][j] = id
				} else if fabric[i][j] != -1 {
					claims[fabric[i][j]].overlapping = true
					fabric[i][j] = -1
					inchesCount++
				}
				if fabric[i][j] == -1 {
					newClaim.overlapping = true
				}
			}
		}
		claims[id] = &newClaim
	}
	fmt.Printf("Part One: square inches of fabric within two or more claims %v\n", inchesCount)

	for id, c := range claims {
		if !c.overlapping {
			fmt.Printf("Part Two: the id of the claim that doesn't overlap is %v\n", id)
		}
	}
}
