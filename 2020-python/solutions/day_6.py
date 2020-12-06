"""AOC Day 6"""

import pathlib
import time
import collections

TEST_INPUT = """abc

a
b
c

ab
ac

a
a
a
a

b"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    groups = input_data.strip().split("\n\n")
    yes_count = list()
    for group in groups:
        persons = group.split("\n")
        yes_count.append((len(persons), collections.Counter(''.join(persons))))
    return yes_count

def part1(entries: list) -> int:
    """part1 solver take a list of sets and return an int"""
    return sum(len(group[1].keys()) for group in entries)


def part2(entries: list) -> int:
    """part2 solver take a list of sets and return an int"""
    count = 0
    for group in entries:
        for key in group[1].keys():
            if group[1][key] == group[0]:
                count += 1
    return count

def test_input():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 11
    assert part2(entries) == 6

def test_bench(benchmark):
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
