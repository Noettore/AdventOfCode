"""AOC 2020 Day 25"""

import pathlib
import time

TEST_INPUT = """5764801
17807724"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    return tuple(map(int, input_data.splitlines()))

def part1(entries: tuple) -> int:
    """part1 solver"""
    card_key, door_key = entries
    loop_size = 0
    key = 1
    while key not in (card_key, door_key):
        loop_size += 1
        key = (key * 7) % 20201227

    if key == card_key:
        return pow(door_key, loop_size, 20201227)
    return pow(card_key, loop_size, 20201227)

def test_input_day_25():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 14897079

def test_bench_day_25(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    print("Part 1: %s" % part1(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
