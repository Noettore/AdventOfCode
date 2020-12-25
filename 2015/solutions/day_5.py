"""AOC 2015 Day 5"""

import pathlib
import time

TEST_INPUT = """ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb"""

TEST_INPUT_2 = """qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    entries = list()
    for line in input_data.split('\n'):
        entries.append(line)
    return entries

def part1(entries: list) -> int:
    """part1 solver"""
    nice_strings = 0
    for string in entries:
        vowels_count = 0
        doubles = False
        forbidden = False
        for index, char in enumerate(string):
            if char in 'aeiou':
                vowels_count += 1
            if not doubles and index < len(string)-1 and char == string[index+1]:
                doubles = True
        for forbidden_substring in ('ab', 'cd', 'pq', 'xy'):
            if forbidden:
                break
            if forbidden_substring in string:
                forbidden = True
        if vowels_count >= 3 and doubles and not forbidden:
            nice_strings += 1
    return nice_strings

def part2(entries: list) -> int:
    """part2 solver"""
    nice_strings = 0
    for string in entries:
        if any([string.count(string[i:i+2]) >= 2 for i in range(len(string)-2)]) and any([string[i] == string[i+2] for i in range(len(string)-2)]):
            nice_strings += 1
    return nice_strings


def test_input_day_5():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 2
    entries = extract(TEST_INPUT_2)
    assert part2(entries) == 2

def test_bench_day_5(benchmark):
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
