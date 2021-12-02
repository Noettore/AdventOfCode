"""AOC Day 2"""

from os import read
import pathlib
import time

TEST_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = list()
    for entry in input_data.split('\n'):
        dir, dist = entry.split(' ')
        dist = int(dist)
        entries.append((dir, dist))
    return entries

def part1(entries: list) -> int:
    """part1 solver take the entries and return the part1 solution"""
    h_pos = 0
    v_pos = 0
    for dir, dist in entries:
        if dir == "forward":
            h_pos += dist
        elif dir == "up":
            v_pos -= dist
        elif dir == "down":
            v_pos += dist
        else:
            return None
    return h_pos*v_pos

def part2(entries: list) -> int:
    """part2 solver take the entries and return the part2 solution"""
    h_pos = 0
    v_pos = 0
    aim = 0
    for dir, dist in entries:
        if dir == "forward":
            h_pos += dist
            v_pos += aim * dist
        elif dir == "up":
            aim -= dist
        elif dir == "down":
            aim += dist
        else:
            return None
    return h_pos*v_pos

def test_input_day_02():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 150
    assert part2(entries) == 900

def test_bench_day_02(benchmark):
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