"""AOC Day 13"""

import pathlib
import time

TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    sheet = set()
    folds = list()
    s_instr, f_instr = input_data.split('\n\n')
    for line in s_instr.split('\n'):
        sheet.add(tuple(map(int, line.split(','))))
    for line in f_instr.split('\n'):
        equal_pos = line.index('=')
        folds.append((line[equal_pos-1], int(line[equal_pos+1:])))
    return (sheet, folds)

def fold(sheet: set, direction: str, axis: int):
    folded = set()

    for x, y in sheet:
        if direction == 'x' and x > axis:
            x = 2 * axis - x
        elif direction == 'y' and y > axis:
            y = 2 * axis - y

        folded.add((x, y))

    return folded

def part1(entries: tuple) -> int:
    """part1 solver take the entries and return the part1 solution"""
    direction, axis = entries[1][0]
    sheet = fold(entries[0], direction, axis)
    return len(sheet)

def part2(entries: tuple) -> str:
    """part2 solver take the entries and return the part2 solution"""
    sheet = entries[0]
    fold_instructions = entries[1]
    for direction, axis in fold_instructions:
        sheet = fold(sheet, direction, axis)
    
    max_x = max(p[0] for p in sheet)
    max_y = max(p[1] for p in sheet)
    out = ''
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            out += '#' if (x, y) in sheet else ' '
        out += '\n'
    return out

def test_input_day_13():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 17

def test_bench_day_13(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    print("Part 1: %d" % part1(entries))
    print("Part 2:\n%s" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
