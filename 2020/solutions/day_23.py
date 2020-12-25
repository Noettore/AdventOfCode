"""AOC 2020 Day 23"""

import pathlib
import time

TEST_INPUT = """389125467"""

class Cup:
    """a cup with a value and a pointer to the next cup"""
    def __init__(self, value):
        self.value = value
        self.next = None

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    return list(map(int, input_data))

def build_list(values: list, n_cups: int = None) -> tuple:
    """return the value of the first cup and a dict of Cup"""
    if n_cups is None:
        n_cups = len(values)
    cups_list = [None]*(n_cups+1)
    for i in range(1, n_cups+1):
        cups_list[i] = Cup(i)

    for i, _ in enumerate(values):
        cups_list[values[i]].next = cups_list[values[(i+1)%len(values)]]

    return values[0], cups_list

def play_crab_cups(first_cup: int, cups: list, moves: int):
    """play n moves of crab cups"""
    current = cups[first_cup]
    max_cup = len(cups) - 1
    for _ in range(moves):
        next_cup = current.next
        picked = (next_cup.value, next_cup.next.value, next_cup.next.next.value)
        current.next = current.next.next.next.next
        label = current.value

        while label in picked or label == current.value:
            if label != 1:
                label = label-1
            else:
                label = max_cup

        destination = cups[label]
        next_cup.next.next.next = destination.next
        destination.next = next_cup
        current = current.next

def part1(entries: list) -> str:
    """part1 solver"""
    first_cup, cups = build_list(entries)
    play_crab_cups(first_cup, cups, 100)

    cur_cup = cups[1]
    cups_str = ''
    for _ in range(8):
        cur_cup = cur_cup.next
        cups_str += str(cur_cup.value)

    return cups_str

def part2(entries: list) -> int:
    """part2 solver"""
    entries.extend(range(10, 1000001))
    first_cup, cups = build_list(entries)
    play_crab_cups(first_cup, cups, 10000000)

    return cups[1].next.value * cups[1].next.next.value

def test_input_day_23():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == '67384529'
    assert part2(entries) == 149245887792

def test_bench_day_23(benchmark):
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
