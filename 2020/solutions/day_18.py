"""AOC 2020 Day 18"""

import pathlib
import time

TEST_INPUT = """1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    return [exp.rstrip() for exp in input_data.split('\n')]

def regular_op(stack: list, num: int) -> list:
    """return the stack after performing a regular math operation"""
    while stack:
        if stack[-1] == '(':
            break
        operator, left_operand = stack[-1], stack[-2]
        stack = stack[:-2]
        if operator == '+':
            num = left_operand + num
        elif operator == '*':
            num = left_operand * num
    stack.append(num)
    return stack

def advanced_op(stack: list, num: int, sub_expr: bool) -> list:
    """return the stack after performing an advanced math operation"""
    if sub_expr:
        index = -1
        for stack_index, value in enumerate(stack):
            if value == '(':
                index = stack_index
        if index != -1:
            target = stack[index+1:]
            stack = stack[:index]
        else:
            target = stack
            stack = []
        for value in target:
            if value != '*':
                num *= int(value)
    while stack:
        if stack[-1] in '(*':
            break
        operator, left_operand = stack[-1], stack[-2]
        stack = stack[:-2]
        if operator == '+':
            num = left_operand + num
    stack.append(num)
    return stack

def evaluate(expression: str, advance: bool = False) -> tuple:
    """return the result of an expression evaluated with regular or advanced math operator precendece"""
    stack = list()
    index = 0
    while index < len(expression):
        data = expression[index]
        if data.isdigit():
            num = int(data)
            if advance:
                stack = advanced_op(stack, num, False)
            else:
                stack = regular_op(stack, num)
        elif data in '*+(':
            stack.append(data)
        elif data == ')':
            num = int(stack[-1])
            if advance:
                stack = stack[:-1]
                stack = advanced_op(stack, num, True)
            else:
                stack = stack[:-2]
                stack = regular_op(stack, num)
        index += 1
    if advance and len(stack) > 1:
        stack = advanced_op(stack[:-1], int(stack[-1]), True)
    return stack[0]

def part1(entries: dict) -> int:
    """part1 solver"""
    result_sum = 0
    for expression in entries:
        result_sum += evaluate(expression)
    return result_sum

def part2(entries: tuple) -> int:
    """part2 solver"""
    result_sum = 0
    for expression in entries:
        result_sum += evaluate(expression, True)
    return result_sum

def test_input_day_18():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 26386
    assert part2(entries) == 693942

def test_bench_day_18(benchmark):
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
