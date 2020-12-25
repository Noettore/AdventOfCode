"""AOC Day 1"""

import pathlib
import time

def read_input(input_path: str) -> tuple:
    """take input file path and return appropriate data structure"""
    with open(input_path, 'r') as input_file:
        entries = list()
        is_present = [False]*2020
        for entry in input_file.readlines():
            entries.append(int(entry))
            is_present[int(entry)-1] = True
        return (entries, is_present)

def part1(entries: list, is_present: list) -> int:
    """part1 solver take a list of int and a list of bool and return an int"""
    for x in entries:
        complement = 2020 - x
        if complement > 0 and is_present[complement-1]:
            return x * complement
    return None

def part2(entries: list, is_present: list) -> int:
    """part2 solver take a list of int and a list of bool and return an int"""
    for x, i in enumerate(entries):
        for y in entries[i:]:
            complement = 2020 - x - y
            if complement > 0 and is_present[complement-1]:
                return x * y * complement
    return None

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    entries, is_present = read_input(input_path)
    start_time = time.time()
    print("Part 1: %d" % part1(entries, is_present))
    print("Part 2: %d" % part2(entries, is_present))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
