"""AOC 2020 Day 11"""

import pathlib
import time
import copy

TEST_INPUT = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

FLOOR = 0
EMPTY_SEAT = 1
OCCUPIED_SEAT = 2

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = []
    for row in input_data.split('\n'):
        entries.append([])
        for seat in row:
            if seat == '.':
                entries[-1].append(FLOOR)
            elif seat == 'L':
                entries[-1].append(EMPTY_SEAT)
            elif seat == '#':
                entries[-1].append(OCCUPIED_SEAT)
            else:
                raise ValueError("Invalid seat %s" % seat)
    return entries

def occupied_adjacent_neighbors(seats: list, row: int, column: int) -> int:
    """return number of occupied adjacent neighbors of a given seat"""
    neigh_seats = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    neighbors = 0
    rows = len(seats)
    columns = len(seats[0])
    for dy, dx in neigh_seats:
        nrow, ncolumn = row+dy, column+dx
        if 0 <= nrow < rows and 0 <= ncolumn < columns and seats[nrow][ncolumn] == OCCUPIED_SEAT:
            neighbors += 1
    return neighbors

def occupied_insight_neighbors(seats: list, row: int, column: int) -> int:
    """return number of occupied in-sight neighbors of a given seat"""
    neigh_seats = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    neighbors = 0
    rows = len(seats)
    columns = len(seats[0])
    for dy, dx in neigh_seats:
        nrow, ncolumn = row+dy, column+dx
        while 0 <= nrow < rows and 0 <= ncolumn < columns:
            seat = seats[nrow][ncolumn]
            if seat == OCCUPIED_SEAT:
                neighbors += 1
                break
            elif seat == EMPTY_SEAT:
                break
            nrow += dy
            ncolumn += dx
    return neighbors

def part1(entries: list) -> int:
    """part1 solver"""
    seats = copy.deepcopy(entries)
    while True:
        new_grid = []
        changed = False
        for y, row in enumerate(seats):
            new_grid.append([])
            for x, seat in enumerate(row):
                neighbors = occupied_adjacent_neighbors(seats, y, x)
                if seat == EMPTY_SEAT and neighbors == 0:
                    new_grid[-1].append(OCCUPIED_SEAT)
                    changed = True
                elif seat == OCCUPIED_SEAT and neighbors >= 4:
                    new_grid[-1].append(EMPTY_SEAT)
                    changed = True
                else:
                    new_grid[-1].append(seat)
        if changed:
            seats = new_grid
        else:
            return sum(row.count(OCCUPIED_SEAT) for row in seats)

def part2(entries: list) -> int:
    """part2 solver"""
    seats = copy.deepcopy(entries)
    while True:
        new_grid = []
        changed = False
        for y, row in enumerate(seats):
            new_grid.append([])
            for x, seat in enumerate(row):
                neighbors = occupied_insight_neighbors(seats, y, x)
                if seat == EMPTY_SEAT and neighbors == 0:
                    new_grid[-1].append(OCCUPIED_SEAT)
                    changed = True
                elif seat == OCCUPIED_SEAT and neighbors >= 5:
                    new_grid[-1].append(EMPTY_SEAT)
                    changed = True
                else:
                    new_grid[-1].append(seat)
        if changed:
            seats = new_grid
        else:
            return sum(row.count(OCCUPIED_SEAT) for row in seats)

def test_input_day_11():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 37
    assert part2(entries) == 26

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
