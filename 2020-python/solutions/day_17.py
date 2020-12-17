"""AOC 2020 Day 17"""

import pathlib
import time
import itertools

TEST_INPUT = """.#.
..#
###"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str, dims: int) -> set:
    """take input data and return the appropriate data structure"""
    alive_cells = set()
    zeros = [0]*(dims-2)
    for x_cell, row in enumerate(input_data.split('\n')):
        for y_cell, cell in enumerate(row):
            if cell == '#':
                alive_cells.add((x_cell, y_cell, *zeros))
    return alive_cells

def count_alive_neighbors(alive_cells: set, coords: tuple) -> int:
    """return the number of alive neighbors of a given cell"""
    alive = 0
    ranges = ((c-1, c, c+1) for c in coords)
    for cell in itertools.product(*ranges):
        if cell in alive_cells:
            alive += 1
    if coords in alive_cells:
        alive -= 1
    return alive

def get_cube_limits(alive_cells: set, dims: int) -> list:
    """return cube bounds incremented for expansion"""
    limits = list()
    for i in range(dims):
        low = float('Inf')
        high = -float('Inf')
        for row in alive_cells:
            if row[i] < low:
                low = row[i]
            elif row[i] > high:
                high = row[i]
        limits.append(range(low-1, high+2))
    return limits

def step_cube(alive_cells: set, dims: int) -> set:
    """return next step alive cells"""
    next_step = set()
    for cell in itertools.product(*get_cube_limits(alive_cells, dims)):
        alive_neighbors = count_alive_neighbors(alive_cells, cell)
        if (cell in alive_cells and alive_neighbors in (2, 3)) or alive_neighbors == 3:
            next_step.add(cell)
    return next_step

def part1(input_data: str) -> int:
    """part1 solver"""
    cube = extract(input_data, 3)
    for _ in range(6):
        cube = step_cube(cube, 3)
    return len(cube)

def part2(input_data: str) -> int:
    """part2 solver"""
    cube = extract(input_data, 4)
    for _ in range(6):
        cube = step_cube(cube, 4)
    return len(cube)

def test_input_day_17():
    """pytest testing function"""
    assert part1(TEST_INPUT) == 112
    assert part2(TEST_INPUT) == 848

def test_bench_day_17(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    print("Part 1: %d" % part1(input_data))
    print("Part 2: %d" % part2(input_data))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
