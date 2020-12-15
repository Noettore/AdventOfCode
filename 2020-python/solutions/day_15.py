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
    entries = input_data.split(',')
    return entries

def part1(entries: dict) -> int:
    """part1 solver"""
    spoken = dict()
    last_spoken = '-1'
    for turn, number in enumerate(entries, 1):
        spoken[number] = [turn]
        last_spoken = number
    for i in range(len(entries)+1, 2020+1):
        if len(spoken.get(last_spoken, [])) < 2:
            spoken.setdefault('0', []).append(i)
            last_spoken = '0'
        else:
            number = str(int(spoken[last_spoken][-1]) - int(spoken[last_spoken][-2]))
            spoken.setdefault(number, []).append(i)
            last_spoken = number
    return int(last_spoken)

def part2(entries: tuple) -> int:
    """part2 solver"""
    spoken = dict()
    last_spoken = '-1'
    for turn, number in enumerate(entries, 1):
        spoken[number] = [turn]
        last_spoken = number
    for i in range(len(entries)+1, 30000000+1):
        if len(spoken.get(last_spoken, [])) < 2:
            spoken.setdefault('0', []).append(i)
            last_spoken = '0'
        else:
            number = str(int(spoken[last_spoken][-1]) - int(spoken[last_spoken][-2]))
            spoken.setdefault(number, []).append(i)
            last_spoken = number
    return int(last_spoken)

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
