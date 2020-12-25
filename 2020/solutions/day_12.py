"""AOC 2020 Day 12"""

import pathlib
import time

TEST_INPUT = """F10
N3
F7
R90
F11"""

LEFT, RIGHT = 'L', 'R'
FORWARD = 'F'
NORTH, SOUTH, EAST, WEST = 'N', 'S', 'E', 'W'

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = []
    for line in input_data.split('\n'):
        instruction = (line[0], int(line[1:]))
        entries.append(instruction)
    return entries

def rotate_ship(direction: str, rotation: str) -> str:
    """rotate the ship"""
    if direction == NORTH:
        return WEST if rotation == LEFT else EAST
    if direction == SOUTH:
        return EAST if rotation == LEFT else WEST
    if direction == EAST:
        return NORTH if rotation == LEFT else SOUTH
    if direction == WEST:
        return SOUTH if rotation == LEFT else NORTH
    return None

def move(direction: str, x: int, y: int, value: int) -> tuple:
    """move the ship or the waypoint"""
    if direction == NORTH:
        return (x, y+value)
    if direction == SOUTH:
        return (x, y-value)
    if direction == EAST:
        return (x+value, y)
    if direction == WEST:
        return (x-value, y)
    return None

def rotate_waypoint(direction: str, x: int, y: int, value: int) -> tuple:
    """rotate waypoint around ship"""
    if (direction == LEFT and value == 90) or (direction == RIGHT and value == 270):
        return (-y, x)
    if ((direction == LEFT and value == 180) or (direction == RIGHT and value == 180)):
        return (-x, -y)
    if ((direction == LEFT and value == 270) or (direction == RIGHT and value == 90)):
        return (y, -x)
    return None

def part1(entries: list) -> int:
    """part1 solver"""
    direction = EAST
    x_ship, y_ship = 0, 0

    for action, value in entries:
        if action == FORWARD:
            x_ship, y_ship = move(direction, x_ship, y_ship, value)
        elif action in (LEFT, RIGHT):
            for _ in range(value//90):
                direction = rotate_ship(direction, action)
        else:
            x_ship, y_ship = move(action, x_ship, y_ship, value)
    return abs(x_ship) + abs(y_ship)

def part2(entries: list) -> int:
    """part2 solver"""
    x_ship, y_ship = 0, 0
    x_wp, y_wp = 10, 1

    for action, value in entries:
        if action == FORWARD:
            x_ship += x_wp * value
            y_ship += y_wp * value
        elif action in (LEFT, RIGHT):
            x_wp, y_wp = rotate_waypoint(action, x_wp, y_wp, value)
        else:
            x_wp, y_wp = move(action, x_wp, y_wp, value)
    return abs(x_ship) + abs(y_ship)

def test_input_day_12():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 25
    assert part2(entries) == 286

def test_bench_day_12(benchmark):
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
