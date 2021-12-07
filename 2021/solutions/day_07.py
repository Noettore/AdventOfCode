"""AOC Day 7"""

import pathlib
import time
from collections import defaultdict

TEST_INPUT = """16,1,2,0,4,2,7,1,2,14"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    return list(map(int, input_data.split(',')))

def fuel2(crabs: list, mean: int) -> int:
    fuel_sum = 0
    for crab in crabs:
        delta = abs(crab - mean)
        fuel_sum += (delta * (delta + 1)) // 2
    
    return fuel_sum

def part1(entries: list) -> int:
    """part1 solver take the entries and return the part1 solution"""
    crabs = sorted(entries)
    middle_crab = crabs[len(crabs)//2]

    return sum(abs(crab - middle_crab) for crab in crabs)

def part2(entries: list) -> int:
    """part2 solver take the entries and return the part2 solution"""
    crabs = sorted(entries)
    mean = sum(crabs)//len(crabs)
    
    return min(fuel2(entries, mean), fuel2(entries, mean+1))

def test_input_day_07():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 37
    assert part2(entries) == 168

def test_bench_day_07(benchmark):
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
