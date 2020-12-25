package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type node struct {
	children []*node
	metadata []int
}

func treeRecursiveBuild(info *[]int) (*node, int) {
	n := &node{}
	metaSum := 0
	childNum := (*info)[0]
	metaNum := (*info)[1]

	*info = (*info)[2:]

	for i := 0; i < childNum; i++ {
		children, s := treeRecursiveBuild(info)
		metaSum += s
		n.children = append(n.children, children)
	}

	for i := 0; i < metaNum; i++ {
		metaSum += (*info)[0]
		n.metadata = append(n.metadata, (*info)[0])
		if len(*info) > 0 {
			*info = (*info)[1:]
		}
	}

	return n, metaSum
}

func (n *node) value() int {
	value := 0
	if len(n.children) == 0 {
		for _, m := range n.metadata {
			value += m
		}
	} else {
		for _, m := range n.metadata {
			if m <= len(n.children) {
				value += n.children[m-1].value()
			}
		}
	}
	return value
}

func main() {
	var info []int
	file, err := os.Open("./input")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scan := bufio.NewScanner(file)
	scan.Scan()
	line := scan.Text()

	for _, n := range strings.Split(line, " ") {
		num, _ := strconv.Atoi(n)
		info = append(info, num)
	}

	root, metaSum := treeRecursiveBuild(&info)

	fmt.Printf("Part One: %v\n", metaSum)

	fmt.Printf("Part Two: %v\n", root.value())

}
