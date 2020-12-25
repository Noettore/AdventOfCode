"""AOC 2020 Day 19"""

import pathlib
import time
import re

TEST_INPUT = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

TEST_INPUT_2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    rules = dict()
    messages = list()
    rules_input, messages_input = input_data.split('\n\n')[0:2]

    for rule_input in rules_input.split('\n'):
        rule_id, rule = rule_input.split(': ')
        rules[rule_id] = rule

    messages = messages_input.split('\n')

    return rules, messages

def get_regxp(rule_num: str, rules: dict):
    rule = rules[rule_num]
    if re.fullmatch('"."', rule):
        return rule[1]
    rule_parts = rule.split(' | ')
    or_rules = []
    for part in rule_parts:
        numbers = part.split(' ')
        or_rules.append(''.join(get_regxp(n, rules) for n in numbers))

    return f"(?:{'|'.join(or_rules)})"

def get_regxp_upd(rule_num: str, rules: dict):
    if rule_num == '8':
        return f"{get_regxp_upd('42', rules)}+"
    elif rule_num == '11':
        rule_11 = (f"{get_regxp_upd('42', rules)}{{{n}}}{get_regxp_upd('31', rules)}{{{n}}}" for n in range(1, 22))
        return f"(?:{'|'.join(rule_11)})"
    
    rule = rules[rule_num]
    if re.fullmatch('"."', rule):
        return rule[1]
    rule_parts = rule.split(' | ')
    or_rules = []
    for part in rule_parts:
        numbers = part.split(' ')
        or_rules.append(''.join(get_regxp_upd(n, rules) for n in numbers))

    return f"(?:{'|'.join(or_rules)})"

def part1(entries: tuple) -> int:
    """part1 solver"""
    rules, messages = entries
    regxp_0 = re.compile(get_regxp('0', rules))
    return sum(regxp_0.fullmatch(x) is not None for x in messages)

def part2(entries: tuple) -> int:
    """part2 solver"""
    rules, messages = entries
    regxp_0 = re.compile(get_regxp_upd('0', rules))
    return sum(regxp_0.fullmatch(x) is not None for x in messages)

def test_input_day_19():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 2
    entries = extract(TEST_INPUT_2)
    assert part2(entries) == 12

def test_bench_day_19(benchmark):
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
