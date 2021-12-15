"""AOC Day 15"""

import pathlib
import time
import heapq
from collections import defaultdict
from math import inf

TEST_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    grid = list()
    for row in input_data.split('\n'):
        grid.append(list(map(int, row)))
    return grid

def neighbors(row: int, column: int, height: int, width: int) -> tuple:
    for inc_row, inc_column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        delta_row, delta_column = (row + inc_row, column + inc_column)
        if 0 <= delta_row < height and 0 <= delta_column < width:
            yield(delta_row, delta_column)

def dijkstra(grid: list) -> int:
    h, w = len(grid), len(grid[0])
    source = (0, 0)
    destination = (h - 1, w - 1)

    queue = [(0, source)]
    min_dists = defaultdict(lambda: inf, {source: 0})
    visited = set()

    while queue:
        dist, node = heapq.heappop(queue)
        if node == destination:
            return dist
        if node in visited:
            continue
        
        visited.add(node)
        r, c = node
        for neighbor in neighbors(r, c, h, w):
            if neighbor in visited:
                continue
            nr, nc = neighbor
            new_dist = dist + grid[nr][nc]
            if new_dist < min_dists[neighbor]:
                min_dists[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))
    return inf

def part1(grid: list) -> int:
    """part1 solver take the entries and return the part1 solution"""
    return dijkstra(grid)[0]

def part2(grid: list) -> int:
    """part2 solver take the entries and return the part2 solution"""
    tile_w = len(grid)
    tile_h = len(grid[0])

    for _ in range(4):
        for row in grid:
            tail = row[-tile_w:]
            row.extend((x + 1) if x < 9 else 1 for x in tail)
    
    for _ in range(4):
        for row in grid[-tile_h:]:
            row = [(x + 1) if x < 9 else 1 for x in row]
            grid.append(row)

    return dijkstra(grid)[0]

def test_input_day_15():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 40
    assert part2(entries) == 315

def test_bench_day_15(benchmark):
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
