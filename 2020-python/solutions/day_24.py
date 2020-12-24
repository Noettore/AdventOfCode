"""AOC 2020 Day 24"""

import pathlib
import time
import cProfile
import re
import operator
import itertools

TEST_INPUT = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

STEPMAP = {
    'e': (1, 0),
    'se': (1, 1),
    'sw': (0, 1),
    'w': (-1, 0),
    'nw': (-1, -1),
    'ne': (0, -1)
}

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> set:
    """take input data and return the appropriate data structure"""
    rexp_steps = re.compile(r'e|se|sw|w|nw|ne')
    tiles_steps = [rexp_steps.findall(line) for line in input_data.split('\n')]

    black_tiles = set()

    for steps in tiles_steps:
        dst_tile = find_dst_tile(steps)
        if dst_tile in black_tiles:
            black_tiles.remove(dst_tile)
        else:
            black_tiles.add(dst_tile)

    return black_tiles

def find_dst_tile(steps: list) -> tuple:
    """calculate the destination tile based on the steps"""
    x_dst, y_dst = 0, 0
    for step in steps:
        d_x, d_y = STEPMAP[step]
        x_dst += d_x
        y_dst += d_y

    return x_dst, y_dst

def count_black_neighbors(tiles: set, x_tile: int, y_tile: int) -> int:
    """return the number of black adjacent tile of a given one"""
    black_neighbors = 0
    for d_x, d_y in STEPMAP.values():
        if (x_tile+d_x, y_tile+d_y) in tiles:
            black_neighbors += 1
    return black_neighbors

def calculate_floor_bounds(tiles: set) -> tuple:
    """return the floor boundaries"""
    min_x = float('Inf')
    max_x = float('-Inf')
    min_y = float('Inf')
    max_y = float('-Inf')

    for x_tile, y_tile in tiles:
        if x_tile < min_x:
            min_x = x_tile
        elif x_tile > max_x:
            max_x = x_tile
        if y_tile < min_y:
            min_y = y_tile
        elif y_tile > max_y:
            max_y = y_tile

    return range(min_x-1, max_x+2), range(min_y-1, max_y+2)

def flip_tiles(tiles: set) -> set:
    """calculate the new daily floor"""
    new_floor = set()

    for tile in itertools.product(*calculate_floor_bounds(tiles)):
        black_neighbors = count_black_neighbors(tiles, *tile)

        if tile in tiles and not (black_neighbors == 0 or black_neighbors > 2):
            new_floor.add(tile)
        elif tile not in tiles and black_neighbors == 2:
            new_floor.add(tile)

    return new_floor

def part1(entries: set) -> int:
    """part1 solver"""
    return len(entries)

def part2(entries: list) -> int:
    """part2 solver"""
    for _ in range(100):
        entries = flip_tiles(entries)

    return len(entries)

def test_input_day_24():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 10
    assert part2(entries) == 2208

def test_bench_day_24(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    print("Part 1: %s" % part1(entries))
    print("Part 2: %s" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
