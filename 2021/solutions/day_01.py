"""AOC Day 1"""

import pathlib
import time

TEST_INPUT = """199
200
208
210
200
207
240
269
260
263"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = list()
    for entry in input_data.split('\n'):
        entries.append(int(entry))
    return entries

def part1(entries: list) -> int:
    """part1 solver take a list of int and return an int"""
    increment = 0
    for i in range(len(entries)-1):
        if entries[i+1] > entries[i]:
            increment += 1
    return increment
    # oneliner not so time efficient
    # return sum(b > a for a, b in zip(entries, entries[1:]))

def part2(entries: list) -> int:
    """part2 solver take a list of int and return an int"""
    increment = 0
    for i in range(len(entries)-3):
        if entries[i+3] > entries[i]:
            increment += 1
    return increment
    # oneliner not so time efficient
    # return sum(b > a for a, b in zip(entries, entries[3:]))

def test_input_day_01():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 7
    assert part2(entries) == 5

def test_bench_day_01(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    print("Part 1: %d" % part1(entries))
    print("Part 2: %d" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()