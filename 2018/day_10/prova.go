package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type point struct {
	x, y   int
	vx, vy int
}

func print(points []*point, xrange, yrange, x, y int) {
	var res = make([][]string, yrange+1)
	for i := range res {
		res[i] = make([]string, xrange+1)
	}
	for i := 0; i < xrange+1; i++ {
		for j := 0; j < yrange+1; j++ {
			res[j][i] = " "
		}
	}
	for _, p := range points {
		res[(*p).y-y][(*p).x-x] = "*"
	}
	fmt.Println("Part 1: ")
	for _, row := range res {
		fmt.Println(row)
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func move(points []*point, x, X, y, Y *int) {
	var tx, tX, ty, tY int = 2147483647, -2147483648, 2147483647, -2147483648
	for _, val := range points {
		(*val).x += (*val).vx
		(*val).y += (*val).vy
		tx = min(tx, (*val).x)
		tX = max(tX, (*val).x)
		ty = min(ty, (*val).y)
		tY = max(tY, (*val).y)
	}
	*x, *X, *y, *Y = tx, tX, ty, tY
}

func main() {

	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var points []*point

	var x, X, y, Y int = 2147483647, -2147483648, 2147483647, -2147483648

	for scanner.Scan() {
		p := new(point)
		line := scanner.Text()
		fmt.Sscanf(line, "position=<%d, %d> velocity=<%d, %d>", &p.x, &p.y, &p.vx, &p.vy)
		points = append(points, p)
		x = min(x, (*p).x)
		X = max(X, (*p).x)
		y = min(y, (*p).y)
		Y = max(Y, (*p).y)
	}

	var minAt, minVal int
	minVal = (X - x) + (Y - y)

	for i := 1; i <= 100000; i++ {
		move(points, &x, &X, &y, &Y)
		current := (X - x) + (Y - y)
		if current < minVal {
			minVal = current
			minAt = i
		}
	}

	var tx, tX, ty, tY int = 2147483647, -2147483648, 2147483647, -2147483648
	for _, p := range points {
		(*p).x = (*p).x - (100000-minAt)*(*p).vx
		(*p).y = (*p).y - (100000-minAt)*(*p).vy
		tx = min(tx, (*p).x)
		tX = max(tX, (*p).x)
		ty = min(ty, (*p).y)
		tY = max(tY, (*p).y)
	}

	print(points, tX-tx, tY-ty, tx, ty)
	fmt.Printf("Part 2: %v\n", minAt)
}
