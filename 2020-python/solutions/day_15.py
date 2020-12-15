"""AOC 2020 Day 15"""

import pathlib
import time

TEST_INPUT = """3,1,2"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = list(map(int, input_data.split(',')))
    return entries

def calculate_last_spoken(numbers: list, turns: int) -> int:
    """calculate the last spoken number at specified turn"""
    spoken = [0]*turns
    last_spoken = -1

    for turn, number in enumerate(numbers, 1):
        spoken[number] = turn
        last_spoken = number

    for prev_turn in range(len(numbers), turns):
        if spoken[last_spoken] != 0:
            current_spoken = prev_turn - spoken[last_spoken]
        else:
            current_spoken = 0
        spoken[last_spoken] = prev_turn
        last_spoken = current_spoken

    return last_spoken

def part1(entries: dict) -> int:
    """part1 solver"""
    return calculate_last_spoken(entries, 2020)

def part2(entries: tuple) -> int:
    """part2 solver"""
    return calculate_last_spoken(entries, 30000000)

def test_input_day_15():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 1836
    assert part2(entries) == 362

def test_bench_day_15(benchmark):
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
