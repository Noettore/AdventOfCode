"""AOC Day 5"""

import pathlib
import time
import collections

TEST_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    lines = list()
    for line in input_data.splitlines():
        a, b = line.split('->')
        ax, ay = map(int, a.split(','))
        bx, by = map(int, b.split(','))
        lines.append((ax, ay, bx, by))
    return lines

def part1(entries: list, space: collections.defaultdict) -> int:
    """part1 solver take the entries and return the part1 solution"""
    for ax, ay, bx, by in entries:
        if ax == bx:
            for y in range(min(ay, by), max(ay, by) + 1):
                space[ax, y] += 1
        elif ay == by:
            for x in range(min(ax, bx), max(ax, bx) + 1):
                space[x, ay] += 1
    
    return sum(v > 1 for v in space.values())


def part2(entries: list, space: collections.defaultdict) -> int:
    """part2 solver take the entries and return the part2 solution"""
    for ax, ay, bx, by in entries:
        if ax != bx and ay != by:
            for i in range(abs(ax-bx)+1):
                if ax < bx:
                    if ay < by:
                        space[ax+i, ay+i] += 1
                    else:
                        space[ax+i, ay-i] += 1
                else:
                    if ay < by:
                        space[ax-i, ay+i] += 1
                    else:
                        space[ax-i, ay-i] += 1
        
    return sum(v > 1 for v in space.values())

def test_input_day_05():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    space = collections.defaultdict(int)
    assert part1(entries, space) == 5
    assert part2(entries, space) == 12

def test_bench_day_05(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    space = collections.defaultdict(int)
    print("Part 1: %d" % part1(entries, space))
    print("Part 2: %d" % part2(entries, space))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
