"""AOC 2020 Day 16"""

import pathlib
import time
import re

TEST_INPUT = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    values_rexp = re.compile(r'([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)')
    rules_str, ticket_str, nearby_tickets_str = input_data.split('\n\n')

    rules = dict()
    nearby_tickets = list()

    for rule in rules_str.split('\n'):
        field, vals = rule.split(': ')
        ranges = values_rexp.match(vals)
        rules[field] = (
            (int(ranges.group(1)), int(ranges.group(2))),
            (int(ranges.group(3)), int(ranges.group(4)))
        )
    my_ticket = list(map(int, ticket_str.split('\n')[1].split(',')))

    for ticket in nearby_tickets_str.split('\n')[1:]:
        nearby_tickets.append(list(map(int, ticket.split(','))))

    return (rules, my_ticket, nearby_tickets)

def check_field(rule: tuple, field: int) -> bool:
    """check if a field is valid given a rule"""
    for min_range, max_range in rule:
        if  min_range <= field <= max_range:
            return True
    return False

def find_invalid_field(rules: dict, ticket: list) -> int:
    """check if a ticket is valid or not"""
    for field in ticket:
        valid = False
        for rule in rules.values():
            valid = check_field(rule, field)
            if valid:
                break
        if not valid:
            return field
    return None

def part1(entries: tuple) -> tuple:
    """part1 solver"""
    rules, _, nearby_tickets = entries
    valid_tickets = list()
    invalid_fields_sum = 0
    for ticket in nearby_tickets:
        invalid_field = find_invalid_field(rules, ticket)
        if invalid_field is not None:
            invalid_fields_sum += invalid_field
        else:
            valid_tickets.append(ticket)
    return valid_tickets, invalid_fields_sum

def part2(rules: dict, my_ticket: list, valid_tickets: list) -> int:
    """part2 solver"""
    acceptable_fields = {key: [] for key in rules.keys()}
    field_map = {key: None for key in rules.keys()}
    departure_values_product = 1

    for name, rule in rules.items():
        for index in range(len(my_ticket)):
            valid = True
            for ticket in valid_tickets:
                if not check_field(rule, ticket[index]):
                    valid = False
                    break
            if valid:
                acceptable_fields[name].append(index)

    while not all(field is not None for field in field_map.values()):
        removed_index = -1
        for name, indexes in acceptable_fields.items():
            if len(indexes) == 1:
                field_map[name] = indexes[0]
                removed_index = indexes[0]
                break
        for name, indexes in acceptable_fields.items():
            if removed_index in indexes:
                acceptable_fields[name].remove(removed_index)

    for name, index in field_map.items():
        if name.startswith('departure'):
            departure_values_product *= my_ticket[index]

    return departure_values_product

def test_input_day_16():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    _, invalid_fields_sum = part1(entries)
    assert invalid_fields_sum == 71

def test_bench_day_16(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    valid_tickets, invalid_fields_sum = part1(entries)
    print("Part 1: %d" % invalid_fields_sum)
    print("Part 2: %d" % part2(entries[0], entries[1], valid_tickets))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
