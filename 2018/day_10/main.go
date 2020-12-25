package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type point struct {
	x, y   int
	Vx, Vy int
}

func main() {
	var points []*point

	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	for scan.Scan() {
		var p *point

		line := scan.Text()
		fmt.Sscanf(line, "position=<%d, %d> velocity=<%d, %d>", &p.x, &p.y, &p.Vx, &p.Vy)

		points = append(points, p)
	}
}
