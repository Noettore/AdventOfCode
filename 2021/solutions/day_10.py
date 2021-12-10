"""AOC Day 10"""

import pathlib
import time
from collections import deque

TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

ILLEGAL_SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
MISSING_SCORE = {')': 1, ']': 2, '}': 3, '>': 4}

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    lines = input_data.split('\n')
    scores = list()
    for line in lines:
        stack = deque()
        for p in line:
            if p == '(':
                stack.append(')')
            elif p == '[':
                stack.append(']')
            elif p == '{':
                stack.append('}')
            elif p == '<':
                stack.append('>')
            elif stack.pop() != p:
                scores.append((ILLEGAL_SCORE[p], 0))
                break
        else:
            missing_score = 0
            while stack:
                missing_score *= 5
                missing_score += MISSING_SCORE[stack.pop()]
            scores.append((0, missing_score))
    return scores

def part1(scores: list) -> int:
    """part1 solver take the entries and return the part1 solution"""
    syntax_error_score = 0
    for score in scores:
        syntax_error_score += score[0]
    return syntax_error_score

def part2(scores: list) -> int:
    """part2 solver take the entries and return the part2 solution"""
    missing_score = list()
    for score in scores:
        if score[1] > 0:
            missing_score.append(score[1])
    missing_score.sort()
    return missing_score[len(missing_score) // 2]

def test_input_day_10():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 26397
    assert part2(entries) == 288957

def test_bench_day_10(benchmark):
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
