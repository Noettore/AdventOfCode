"""AOC Day 5"""

import pathlib
import time

def read_input(input_path: str) -> list:
    """take input file path and return appropriate data structure"""
    with open(input_path, 'r') as input_file:
        entries = input_file.readlines()
        seats = list()
        for entry in entries:
            entry = entry.strip()
            row = ''.join(['0' if letter == 'F' else '1' for letter in entry[:7]])
            column = ''.join(['0' if letter == 'L' else '1' for letter in entry[-3:]])
            seat = int(row, 2) * 8 + int(column, 2)
            seats.append(seat)
        seats.sort()
        return seats



def part1(entries: list) -> int:
    """part1 solver take a list of strings and return an int"""
    return max(entries)


def part2(entries: list) -> int:
    """part2 solver take a list of strings and return an int"""
    missing = [seat for seat in range(entries[0], entries[-1]) if seat not in entries]
    return missing[0]

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    entries = read_input(input_path)
    print("Part 1: %d" % part1(entries))
    print("Part 2: %d" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))


if __name__ == "__main__":
    main()
