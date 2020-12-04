"""AOC Day 2"""

import pathlib
import time
import re

def read_input(input_path: str) -> list:
    """take input file path and return appropriate data structure"""
    with open(input_path, 'r') as input_file:
        rules = list()
        for entry in input_file.readlines():
            splitted = re.split('-| |: ', entry)
            rule = [int(splitted[0]), int(splitted[1]), splitted[2], splitted[3]]
            rules.append(rule)
        return rules


def part1(entries: list) -> int:
    """part1 solver take a list of tuples and return an int"""
    correct_passwords = 0
    for entry in entries:
        occurrences = entry[3].count(entry[2])
        if occurrences in range(entry[0], entry[1]+1):
            correct_passwords += 1
    return correct_passwords


def part2(entries: list) -> int:
    """part2 solver take a list of tuples and return an int"""
    correct_passwords = 0
    for entry in entries:
        pos_1, pos_2, letter, password = entry[:]
        if (password[pos_1-1] == letter) != (password[pos_2-1] == letter):
            correct_passwords += 1
    return correct_passwords

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    entries = read_input(input_path)
    start_time = time.time()
    print("Part 1: %d" % part1(entries))
    print("Part 2: %d" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))


if __name__ == "__main__":
    main()
