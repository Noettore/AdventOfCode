"""AOC 2020 Day 9"""

import pathlib
import time
import itertools

TEST_INPUT = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = list()
    for entry in input_data.split('\n'):
        entries.append(int(entry))
    return entries

def part1(entries: list, preamble_length: int) -> int:
    """part1 solver"""
    for index, entry in enumerate(entries[preamble_length:]):
        preamble = entries[index:index+preamble_length]
        if entry not in [i+j for i, j in itertools.combinations(preamble, 2)]:
            return entry
    return None

def part2(entries: list, invalid_number: int) -> int:
    """part2 solver"""
    left, right = 0, 1
    interval_sum = entries[left] + entries[right]
    while True:
        if interval_sum < invalid_number:
            right += 1
            interval_sum += entries[right]
        elif interval_sum > invalid_number:
            interval_sum -= entries[left]
            left += 1
        else:
            return min(entries[left:right+1]) + max(entries[left:right+1])

def test_input_day_9():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries, 5) == 127
    assert part2(entries, 127) == 62

def test_bench_day_9(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    invalid_number = part1(entries, 25)
    print("Part 1: %d" % invalid_number)
    print("Part 2: %d" % part2(entries, invalid_number))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
