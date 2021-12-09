"""AOC Day 8"""

import pathlib
import time

TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    patterns = list()
    digits = list()
    for line in input_data.split('\n'):
        pattern, digit = line.split('|')
        patterns.append(pattern.split())
        digits.append(digit.split())
    return (patterns, digits)

def find_digit(patterns: list) -> dict:
    p2d = dict()
    for pattern in patterns:
        pattern = frozenset(pattern)
        p_len = len(pattern)
        if p_len == 2:
            p2d[pattern] = 1
        elif p_len == 3:
            p2d[pattern] = 7
        elif p_len == 4:
            p2d[pattern] = 4
        elif p_len == 7:
            p2d[pattern] = 8

    d2p = {value: key for key, value in p2d.items()}
    
    for pattern in patterns:
        p_len = len(pattern)
        if pattern not in p2d:
            pattern = frozenset(pattern)
            if p_len == 5:
                if len(pattern.intersection(d2p[1])) == 2:
                    p2d[pattern] = 3
                elif len(pattern.intersection(d2p[4])) == 3:
                    p2d[pattern] = 5
                else:
                    p2d[pattern] = 2
            elif p_len == 6:
                if len(pattern.intersection(d2p[4])) == 4:
                    p2d[pattern] = 9
                elif len(pattern.intersection(d2p[7])) == 2:
                    p2d[pattern] = 6
                else:
                    p2d[pattern] = 0
    return p2d

def part1(entries: tuple) -> int:
    """part1 solver take the entries and return the part1 solution"""
    count = 0
    for line in entries[1]:
        for digit in line:
            if len(digit) in {2, 3, 4, 7}:
                count += 1
    return count

def part2(entries: tuple) -> int:
    """part2 solver take the entries and return the part2 solution"""
    sum = 0
    for i, patterns in enumerate(entries[0]):
        digits = entries[1][i]
        pattern_to_digit = find_digit(patterns)
        
        sum += pattern_to_digit[frozenset(digits[0])] * 1000
        sum += pattern_to_digit[frozenset(digits[1])] * 100
        sum += pattern_to_digit[frozenset(digits[2])] * 10
        sum += pattern_to_digit[frozenset(digits[3])]
    return sum

def test_input_day_08():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 26
    assert part2(entries) == 61229

def test_bench_day_08(benchmark):
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
