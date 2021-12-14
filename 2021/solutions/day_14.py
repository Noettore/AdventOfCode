"""AOC Day 14"""

import pathlib
import time
from collections import defaultdict

TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    template, insertion_rules_data = input_data.split('\n\n')
    insertion_rules = {}
    polymer = defaultdict(int)
    for line in insertion_rules_data.split('\n'):
        (a, b), c = line.split(' -> ')
        insertion_rules[a, b] = ((a, c), (c, b))
    for pair in zip(template, template[1:]):
        polymer[pair] += 1
    
    return (template, polymer, insertion_rules)

def react(polymer: defaultdict, rules: dict, reaction_num: int, last_elem: str) -> defaultdict:
    for _ in range(reaction_num):
        new_polymer = defaultdict(int)
        for pair in polymer:
            products = rules.get(pair)
            if products:
                n = polymer[pair]
                new_polymer[products[0]] += n
                new_polymer[products[1]] += n
            else:
                new_polymer[pair] = polymer[pair]
        polymer = new_polymer
    
    counts = defaultdict(int, {last_elem: 1})
    for (a, _), n in polymer.items():
        counts[a] += n
    
    return polymer, max(counts.values()) - min(counts.values())

def part1(entries: tuple) -> int:
    """part1 solver take the entries and return the part1 solution"""
    template, polymer, rules = entries
    _, solution = react(polymer, rules, 10, template[-1])
    return solution

def part2(entries: tuple) -> int:
    """part2 solver take the entries and return the part2 solution"""
    template, polymer, rules = entries
    _, solution = react(polymer, rules, 40, template[-1])
    return solution

def test_input_day_14():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 1588
    assert part2(entries) == 2188189693529

def test_bench_day_14(benchmark):
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
