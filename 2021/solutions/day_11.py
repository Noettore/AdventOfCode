"""AOC Day 11"""

import pathlib
import time

TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    lines = input_data.split('\n')
    return list(list(map(int, row)) for row in lines)

def neighbors(row: int, column: int, height: int, width: int) -> tuple:
    deltas = (
        (1, 0), (-1, 0),
        (0, 1), (0, -1),
        (1, 1), (1, -1),
        (-1, 1), (-1, -1)
    )

    for delta_row, delta_column in deltas:
        inc_row, inc_column = (row + delta_row, column + delta_column)
        if 0 <= inc_row < height and 0 <= inc_column < width:
            yield inc_row, inc_column

def flash(grid: list, row: int, column: int, height: int, width: int):
    if grid[row][column] > 9:
        grid[row][column] = -1
        for n_row, n_column in neighbors(row, column, height, width):
            if grid[n_row][n_column] != -1:
                grid[n_row][n_column] += 1
                flash(grid, n_row, n_column, height, width)

def step(grid: list, height: int, width: int) -> int:
    flashes = 0

    for row in range(height):
        for column in range(width):
            grid[row][column] += 1

    for row in range(height):
        for column in range(width):
            flash(grid, row, column, height, width)
    
    for row in range(height):
        for column in range(width):
            if grid[row][column] == -1:
                grid[row][column] = 0
                flashes += 1
    
    return flashes

def part1(grid: list) -> int:
    """part1 solver take the entries and return the part1 solution"""
    height, width = len(grid), len(grid[0])
    flashes = sum(step(grid, height, width) for _ in range(100))

    return flashes

def part2(grid: list) -> int:
    """part2 solver take the entries and return the part2 solution"""
    num_step = 101
    height, width = len(grid), len(grid[0])
    num_cells = height * width
    while True:
        if step(grid, height, width) == num_cells:
            return num_step
        num_step += 1


def test_input_day_11():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 1656
    assert part2(entries) == 195

def test_bench_day_11(benchmark):
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
