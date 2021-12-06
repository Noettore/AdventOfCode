"""AOC Day 6"""

import pathlib
import time
from collections import defaultdict

TEST_INPUT = """3,4,3,1,2"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> defaultdict:
    """take input data and return the appropriate data structure"""
    timers = map(int, input_data.split(','))
    fish = defaultdict(int)

    for t in timers:
        fish[t] += 1
    
    return fish

def calculate(fish: defaultdict, days: int) -> defaultdict:
    for _ in range(days):
        new_fish = defaultdict(int)
        
        for timer, num in fish.items():
            timer -= 1
            if timer < 0:
                new_fish[6] += num
                new_fish[8] += num
            else:
                new_fish[timer] += num
        
        fish = new_fish
    
    return sum(fish.values())

def part1(entries: defaultdict) -> int:
    """part1 solver take the entries and return the part1 solution"""
    return calculate(entries, 80)

def part2(entries: defaultdict) -> int:
    """part2 solver take the entries and return the part2 solution"""
    return calculate(entries, 256)

def test_input_day_06():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 5934
    assert part2(entries) == 26984457539

def test_bench_day_06(benchmark):
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
