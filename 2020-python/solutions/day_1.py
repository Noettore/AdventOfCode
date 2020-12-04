"""AOC Day 1"""

import pathlib
import time

def read_input(input_path: str) -> list:
    """take input file path and return appropriate data structure"""
    with open(input_path, 'r') as input_file:
        entries = list()
        for entry in input_file.readlines():
            entries.append(int(entry))
        return entries

def part1(entries: list) -> int:
    """part1 solver take a list of int and return an int"""
    for x in entries:
        complement = 2020 - x
        if complement in entries:
            return x * complement
    return None

def part2(entries: list) -> int:
    """part2 solver take a list of int and return an int"""
    for x, i in enumerate(entries):
        for y in entries[i:]:
            complement = 2020 - x - y
            if complement in entries:
                return x * y * complement
    return None


def main():
    """main function"""
    input_path = str(pathlib.Path.cwd()) + "/inputs/" + str(pathlib.Path(__file__).stem)
    entries = read_input(input_path)
    start_time = time.time()
    print("Part 1: %d" % part1(entries))
    print("Part 2: %d" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
