"""AOC 2015 Day 6"""

import pathlib
import time
import re
import numpy

TEST_INPUT = """turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    entries = list()
    for line in input_data.split('\n'):
        instructions = re.match(r"(\D+)(\d+),(\d+)[\D]+(\d+),(\d+)", line).groups()
        entries.append((instructions[0].strip(), int(instructions[1]), int(instructions[2]), int(instructions[3]), int(instructions[4])))
    return entries

def part1(entries: list) -> int:
    """part1 solver"""
    grid = numpy.zeros((1000, 1000), 'int32')
    for instruction in entries:
        cmd, x1, y1, x2, y2 = instruction
        if cmd == "turn on":
            grid[x1:x2+1, y1:y2+1] = 1
        elif cmd == "turn off":
            grid[x1:x2+1, y1:y2+1] = 0
        elif cmd == "toggle":
            grid[x1:x2+1, y1:y2+1] = numpy.logical_not(grid[x1:x2+1, y1:y2+1])
    return numpy.sum(grid)

def part2(entries: list) -> int:
    """part2 solver"""
    grid = numpy.zeros((1000, 1000), 'int32')
    for instruction in entries:
        cmd, x1, y1, x2, y2 = instruction
        if cmd == "turn on":
            grid[x1:x2+1, y1:y2+1] += 1
        elif cmd == "turn off":
            grid[x1:x2+1, y1:y2+1] -= 1
            grid[grid < 0] = 0
        elif cmd == "toggle":
            grid[x1:x2+1, y1:y2+1] += 2
    return numpy.sum(grid)

def test_input_day_6():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 998996
    assert part2(entries) == 1001996

def test_bench_day_6(benchmark):
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
