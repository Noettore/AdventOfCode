"""AOC Day 9"""

import pathlib
import time
from collections import deque

TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    grid = list()
    for row in input_data.split('\n'):
        grid.append(tuple(map(int, row)))
    return tuple(grid)

def neighbors(row: int, column: int, height: int, width: int) -> tuple:
    for inc_row, inc_column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        delta_row, delta_column = (row + inc_row, column + inc_column)
        if 0 <= delta_row < height and 0 <= delta_column < width:
            yield(delta_row, delta_column)

def bfs(grid: tuple, row: int, column: int, height: int, width: int) -> set:
    queue = deque([(row, column)])
    visited = set()

    while queue:
        cur_cell = queue.popleft()
        if cur_cell in visited:
            continue
        visited.add(cur_cell)
        for nr, nc in neighbors(*cur_cell, height, width):
            if grid[nr][nc] != 9 and (nr, nc) not in visited:
                queue.append((nr, nc))
    return visited

def basin_sizes(grid: tuple, height: int, width: int) -> int:
    visited = set()
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 9 and (r, c) not in visited:
                basin = bfs(grid, r, c, height, width)
                visited = visited.union(basin)
                yield len(basin)

def part1(grid: tuple) -> int:
    """part1 solver take the entries and return the part1 solution"""
    h = len(grid)
    w = len(grid[0])
    sum = 0

    for r, row in enumerate(grid):
        for c, cell  in enumerate(row):
            lowest = True
            for nr, nc in neighbors(r, c, h, w):
                if grid[nr][nc] <= cell:
                    lowest = False
            if lowest:
                sum += cell + 1
    return sum

def part2(grid: tuple) -> int:
    """part2 solver take the entries and return the part2 solution"""
    h = len(grid)
    w = len(grid[0])
    
    sizes = sorted(basin_sizes(grid, h, w), reverse=True)
    return sizes[0]*sizes[1]*sizes[2]

def test_input_day_09():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 15
    assert part2(entries) == 1134

def test_bench_day_09(benchmark):
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
