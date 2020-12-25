"""AOC 2020 Day 8"""

import pathlib
import time

TEST_INPUT = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

class Instruction:
    """Instruction class hold an operation, an argument and an execution counter"""
    op = None
    arg = None

    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    instructions = list()
    for instruction in input_data.split('\n'):
        op, arg = instruction.split(' ')
        arg = int(arg)
        assert op in ('acc', 'jmp', 'nop')
        instructions.append(Instruction(op, arg))
    return instructions

def run(entries: list) -> (int, bool):
    """run instructions"""
    instruction_counter = 0
    prev_instruction_counter = 0
    accumulator = 0
    exec_counter = [0]*len(entries)
    while instruction_counter < len(entries):
        prev_instruction_counter = instruction_counter
        instruction = entries[instruction_counter]

        if exec_counter[instruction_counter] != 0:
            return accumulator, False

        if instruction.op == 'nop':
            instruction_counter += 1
        elif instruction.op == 'acc':
            accumulator += instruction.arg
            instruction_counter += 1
        elif instruction.op == 'jmp':
            instruction_counter += instruction.arg
        else:
            raise ValueError('Invalid instruction operation %s' % instruction.op)

        exec_counter[prev_instruction_counter] += 1

    return accumulator, True

def part1(entries: list) -> int:
    """part1 solver"""
    return run(entries)[0]

def part2(entries: list) -> int:
    """part2 solver"""
    for instruction in entries:
        if instruction.op == 'acc':
            continue
        original_instruction = instruction.op
        instruction.op = 'jmp' if instruction.op == 'nop' else 'nop'
        accumulator, success = run(entries)
        if success:
            return accumulator
        instruction.op = original_instruction

def test_input_day_8():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 5
    assert part2(entries) == 8

def test_bench_day_8(benchmark):
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
