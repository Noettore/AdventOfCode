package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type marble struct {
	left  *marble
	right *marble
	value uint64
}

func (m *marble) placeMarble(newMarbleValue uint64) *marble {
	var newMarble = marble{left: m.right, right: m.right.right, value: newMarbleValue}

	m.right.right.left = &newMarble
	m.right.right = &newMarble

	return &newMarble
}

func (m *marble) removeCurrentMarble() (*marble, uint64) {
	val := m.value

	m.left.right = m.right
	m.right.left = m.left

	return m.right, val
}

func (m *marble) changeCurrentMarble(clockwiseMove int) *marble {
	var newCurrentMarble = m
	if clockwiseMove > 0 {
		for i := 0; i < clockwiseMove; i++ {
			newCurrentMarble = newCurrentMarble.right
		}
	} else {
		for i := 0; i > clockwiseMove; i-- {
			newCurrentMarble = newCurrentMarble.left
		}
	}
	return newCurrentMarble
}

func main() {
	var elfs, currentElf int
	var currentMarbleValue, lastMarbleValue, maxPoint uint64
	var currentMarble = &marble{left: nil, right: nil, value: 0}
	elfsPoint := make(map[int]uint64)

	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	scan.Scan()
	line := scan.Text()
	fmt.Sscanf(line, "%d players; last marble is worth %d points", &elfs, &lastMarbleValue)

	//Part Two: uncomment next line
	//lastMarbleValue *= 100

	for i := 0; i < elfs; i++ {
		elfsPoint[i] = 0
	}

	currentMarble.left = currentMarble
	currentMarble.right = currentMarble

	for currentMarbleValue < lastMarbleValue {
		currentMarbleValue++
		if currentMarbleValue%23 == 0 {
			var val uint64
			currentMarble = currentMarble.changeCurrentMarble(-7)
			currentMarble, val = currentMarble.removeCurrentMarble()
			elfsPoint[currentElf] += (currentMarbleValue + val)
			if elfsPoint[currentElf] > maxPoint {
				maxPoint = elfsPoint[currentElf]
			}
		} else {
			currentMarble = currentMarble.placeMarble(currentMarbleValue)
		}
		currentElf = (currentElf + 1) % elfs
	}

	fmt.Printf("Part One/Two: %v\n", maxPoint)

}
