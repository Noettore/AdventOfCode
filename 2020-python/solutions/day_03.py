"""AOC Day 3"""

import pathlib
import time

def read_input(input_path: str) -> list:
    """take input file path and return appropriate data structure"""
    with open(input_path, 'r') as input_file:
        lines = list()
        for line in input_file.readlines():
            lines.append(line.strip())
        return lines


def slope_tree_check(lines: list, dx: int, dy: int) -> int:
    """check how many trees would be encountered with a specific slope"""
    x_pos = 0
    y_pos = 0
    trees_encountered = 0
    line_length = len(lines[0])
    while y_pos < len(lines):
        if lines[y_pos][x_pos] == '#':
            trees_encountered += 1
        x_pos = (x_pos + dx) % line_length
        y_pos += dy
    return trees_encountered

def part1(entries: list) -> int:
    """part1 solver take a list of strings and return an int"""
    return slope_tree_check(entries, 3, 1)


def part2(entries: list) -> int:
    """part2 solver take a list of tuples and return an int"""
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
        ]
    prod = 1
    for slope in slopes:
        prod *= slope_tree_check(entries, slope[0], slope[1])
    return prod

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    entries = read_input(input_path)
    start_time = time.time()
    print("Part 1: %d" % part1(entries))
    print("Part 2: %d" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))


if __name__ == "__main__":
    main()
