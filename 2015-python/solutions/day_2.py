"""AOC 2015 Day 1"""

import pathlib
import time

TEST_INPUT = """2x3x4
1x1x10"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    gifts = list()
    for gift in input_data.split('\n'):
        dims = tuple(int(dim) for dim in gift.split('x'))
        gifts.append(dims)
    return gifts

def part1(entries: list) -> int:
    """part1 solver take a list and return an int"""
    feet = 0
    for gift in entries:
        (length, width, height) = gift
        side1 = length*width
        side2 = length*height
        side3 = width*height
        feet += 2 * (side1 + side2 + side3) + min(side1, side2, side3)
    return feet

def part2(entries: list) -> int:
    """part2 solver take a list and return an int"""
    feet = 0
    for gift in entries:
        (length, width, height) = gift
        mins = list(gift)
        mins.remove(max(gift))
        feet += length*width*height + 2*sum(mins)
    return feet

def test_input_day_2():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 101
    assert part2(entries) == 48

def test_bench_day_2(benchmark):
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
