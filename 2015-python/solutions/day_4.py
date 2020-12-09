"""AOC 2015 Day 4"""

import pathlib
import time
import hashlib

TEST_INPUT = """abcdef"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def part1(secret: str) -> int:
    """part1 solver"""
    number = 1
    while True:
        key = secret + str(number)
        md5 = hashlib.md5(key.encode()).hexdigest()
        if md5.startswith('00000'):
            return number
        number += 1

def part2(secret: list) -> int:
    """part2 solver"""
    number = 1
    while True:
        key = secret + str(number)
        md5 = hashlib.md5(key.encode()).hexdigest()
        if md5.startswith('000000'):
            return number
        number += 1

def test_input_day_4():
    """pytest testing function"""
    assert part1(TEST_INPUT) == 609043
    assert part2(TEST_INPUT) == 6742839

def test_bench_day_4(benchmark):
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
