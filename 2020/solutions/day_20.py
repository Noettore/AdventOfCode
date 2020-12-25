"""AOC 2020 Day 20"""

import pathlib
import time
import collections
import operator
import itertools

TEST_INPUT = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

MONSTER_PATTERN = (
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
)

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> dict:
    """take input data and return the appropriate data structure"""
    tiles = dict()
    for tile in input_data.split('\n\n'):
        parts = tile.split('\n')
        tile_id = int(parts[0][5:-1])
        tiles[tile_id] = parts[1:]
    return tiles

def edge(matrix: list, side: str) -> str:
    """return a side of a matrix"""
    if side == 'n':
        return matrix[0]
    if side == 's':
        return matrix[-1]
    if side == 'e':
        return ''.join(map(operator.itemgetter(-1), matrix))
    return ''.join(map(operator.itemgetter(0), matrix))

def get_tiles_corners(tiles: dict) -> dict:
    """return the corners of a set of tiles"""
    matching_sides = collections.defaultdict(str)
    corners = {}

    for id_tile1, id_tile2 in itertools.combinations(tiles, 2):
        tile1, tile2 = tiles[id_tile1], tiles[id_tile2]

        for side_a in 'nsew':
            for side_b in 'nsew':
                edge_a, edge_b = edge(tile1, side_a), edge(tile2, side_b)

                if edge_a == edge_b or edge_a == edge_b[::-1]:
                    matching_sides[id_tile1] += side_a
                    matching_sides[id_tile2] += side_b

    for tid, sides in matching_sides.items():
        if len(sides) == 2:
            corners[tid] = sides

    assert len(corners) == 4
    return corners

def rotate90(matrix: list) -> tuple:
    """return the matrix rotated by 90"""
    return tuple(''.join(column)[::-1] for column in zip(*matrix))

def possible_orientations(matrix: list) -> list:
    """return all possible orientations of a given matrix"""
    orientations = [matrix]
    for _ in range(3):
        matrix = rotate90(matrix)
        orientations.append(matrix)
    return orientations

def possible_arrangements(matrix: list) -> list:
    """return all possible arrangements of a given matrix"""
    arrangements = possible_orientations(matrix)
    arrangements.extend(possible_orientations(matrix[::-1]))
    return arrangements

def strip_edges(matrix: list) -> list:
    """return a matrix without it's edges"""
    return [row[1:-1] for row in matrix[1:-1]]

def matching_tile(tile: list, tiles: dict, side_a: str, side_b: str) -> list:
    """return the adjacent tile of a given one"""
    edge_a = edge(tile, side_a)

    for other_id, other_tile in tiles.items():
        if tile is other_tile:
            continue

        for other_arr in possible_arrangements(other_tile):
            if edge_a == edge(other_arr, side_b):
                tiles.pop(other_id)
                return other_arr

def matching_row(prev: list, tiles: dict, tiles_per_row: int) -> list:
    """return matching tiles in the row of a given one"""
    matching_tiles = [prev]
    tile = prev
    for _ in range(tiles_per_row - 1):
        tile = matching_tile(tile, tiles, 'e', 'w')
        matching_tiles.append(tile)
    return matching_tiles

def build_image(top_left_tile: list, tiles: dict, image_dimension: int) -> list:
    """build an image of a set of tiles"""
    first = top_left_tile
    image = []

    while 1:
        image_row = matching_row(first, tiles, image_dimension)
        image_row = map(strip_edges, image_row)
        image.extend(map(''.join, zip(*image_row)))

        if not tiles:
            break

        first = matching_tile(first, tiles, 's', 'n')

    return image

def count_pattern(image: list, pattern: tuple) -> int:
    """return the number of times a given pattern appears in an image"""
    pattern_h, pattern_w = len(pattern), len(pattern[0])
    image_sz = len(image)
    deltas = []

    for row_index, row in enumerate(pattern):
        for cell_index, cell in enumerate(row):
            if cell == '#':
                deltas.append((row_index, cell_index))

    for img in possible_arrangements(image):
        appearances = 0
        for row_index in range(image_sz - pattern_h):
            for cell_index in range(image_sz - pattern_w):
                if all(img[row_index + dr][cell_index + dc] == '#' for dr, dc in deltas):
                    appearances += 1

        if appearances != 0:
            return appearances

def part1(entries: dict) -> int:
    """part1 solver"""
    corners = get_tiles_corners(entries)
    corners_prod = 1
    for tile_id in corners:
        corners_prod *= tile_id
    return corners_prod

def part2(entries: dict) -> int:
    """part2 solver"""
    corners = get_tiles_corners(entries)
    top_left_id, matching_sides = corners.popitem()
    top_left = entries[top_left_id]

    if matching_sides in ('ne', 'en'):
        top_left = rotate90(top_left)
    elif matching_sides in ('nw', 'wn'):
        top_left = rotate90(rotate90(top_left))
    elif matching_sides in ('sw', 'ws'):
        top_left = rotate90(rotate90(rotate90(top_left)))

    image_dimension = int(len(entries) ** 0.5)
    entries.pop(top_left_id)

    image = build_image(top_left, entries, image_dimension)
    monster_cells = sum(row.count('#') for row in MONSTER_PATTERN)
    water_cells = sum(row.count('#') for row in image)
    n_monsters = count_pattern(image, MONSTER_PATTERN)

    return water_cells - n_monsters * monster_cells

def test_input_day_20():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 20899048083289
    assert part2(entries) == 273

def test_bench_day_20(benchmark):
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
