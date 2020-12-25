"""AOC 2015 Day 3"""

import pathlib
import time

TEST_INPUT = """^v^v^v^v^v"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

moves = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}

def part1(entries: str) -> int:
    """part1 solver take a str and return an int"""
    houses = {(0, 0): 1}
    pos_x, pos_y = 0, 0
    for direction in entries:
        delta_x, delta_y = moves[direction]
        pos_x += delta_x
        pos_y += delta_y
        houses[(pos_x, pos_y)] = houses.get((pos_x, pos_y), 0) + 1
    return len(houses)

def part2(entries: str) -> int:
    """part2 solver take a str and return an int"""
    houses = {(0, 0): 2}
    pos_x_santa, pos_y_santa = 0, 0
    pos_x_robot, pos_y_robot = 0, 0
    for index, direction in enumerate(entries):
        delta_x, delta_y = moves[direction]
        if index%2 == 0:
            pos_x_santa += delta_x
            pos_y_santa += delta_y
            houses[(pos_x_santa, pos_y_santa)] = houses.get((pos_x_santa, pos_y_santa), 0) + 1
        else:
            pos_x_robot += delta_x
            pos_y_robot += delta_y
            houses[(pos_x_robot, pos_y_robot)] = houses.get((pos_x_robot, pos_y_robot), 0) + 1
    return len(houses)

def test_input_day_3():
    """pytest testing function"""
    assert part1(TEST_INPUT) == 2
    assert part2(TEST_INPUT) == 11

def test_bench_day_3(benchmark):
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
