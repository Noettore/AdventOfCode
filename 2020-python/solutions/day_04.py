"""AOC Day 4"""

import pathlib
import time
import re

def read_input(input_path: str) -> list:
    """take input file path and return appropriate data structure"""
    with open(input_path, 'r') as input_file:
        data = input_file.read()
        entries = re.split(r"(?:\r?\n){2,}", data.strip())
        passports = list()
        for entry in entries:
            passport = dict()
            entry = entry.replace('\n', ' ')
            data = entry.split(' ')
            for field in data:
                key, value = field.split(':')[:2]
                passport[key] = value
            passports.append(passport)
        return passports

def check_fields(passport: dict) -> bool:
    """check if a passport contains all the required fields"""
    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for required_field in required_fields:
        if required_field not in passport.keys():
            return False
        elif passport[required_field] == None or passport[required_field] == '':
            return False
    return True

def check_data(passport: dict) -> bool:
    """check if all passport fields contains correct data"""
    return (1920 <= int(passport["byr"]) <= 2002 and
        2010 <= int(passport["iyr"]) <= 2020 and
        2020 <= int(passport["eyr"]) <= 2030 and
        ((passport["hgt"].endswith("cm") and 150 <= int(passport["hgt"][:-2]) <= 193) or (passport["hgt"].endswith("in") and 59 <= int(passport["hgt"][:-2]) <= 76)) and
        re.match(r"^#[0-9a-f]{6}$", passport["hcl"]) and
        passport["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth") and
        re.match(r"^[0-9]{9}$", passport["pid"]))

def part1(entries: list) -> int:
    """part1 solver take a list of strings and return an int"""
    valid_passports = 0
    for passport in entries:
        if check_fields(passport):
            valid_passports += 1
    return valid_passports


def part2(entries: list) -> int:
    """part2 solver take a list of tuples and return an int"""
    valid_passports = 0
    for passport in entries:
        if check_fields(passport) and check_data(passport):
            valid_passports += 1
    return valid_passports

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
