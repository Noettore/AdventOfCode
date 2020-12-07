"""AOC 2015 Day 1"""

import pathlib
import time

TEST_INPUT = """))((((("""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def part1(input_data: str) -> int:
    """part1 solver take a str and return an int"""
    return sum(1 if char == '(' else -1 for char in input_data)

def part2(input_data: str) -> int:
    """part2 solver take a dict of dicts and return an int"""
    floor = 0
    for index, char in enumerate(input_data, 1):
        if char == '(':
            floor += 1
        else:
            floor -=1
        if floor == -1:
            return index
    return -1

def test_input_day_1():
    """pytest testing function"""
    assert part1(TEST_INPUT) == 3
    assert part2(TEST_INPUT) == 1

def test_bench_day_2(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    print("Part 1: %d" % part1(input_data))
    print("Part 2: %d" % part2(input_data))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
