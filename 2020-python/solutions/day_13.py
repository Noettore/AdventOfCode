"""AOC 2020 Day 13"""

import pathlib
import time

TEST_INPUT = """939
7,13,x,x,59,x,31,19"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    entries = input_data.split('\n')
    departure_ts = int(entries[0])
    timetable = entries[1].split(',')
    ids = [(-index, int(bus_id)) for index, bus_id in enumerate(timetable) if bus_id != 'x']
    return (departure_ts, ids)

def egcd(a, b):
    """"extended euclidean algorithm"""
    if a == 0:
        return (b, 0, 1)

    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(x, m):
    """calculate the modular multiplicative inverse"""
    g, inv, _ = egcd(x, m)
    assert g == 1
    return inv % m

def part1(entries: tuple) -> int:
    """part1 solver"""
    wait_time = float('inf')
    best_bus_id = -1
    min_dep_time = entries[0]
    for _, bus_id in entries[1]:
        if min_dep_time % bus_id == 0:
            multiple = min_dep_time // bus_id
        else:
            multiple = (min_dep_time // bus_id) + 1
        time_diff = (bus_id * multiple) - min_dep_time
        if time_diff < wait_time:
            wait_time = time_diff
            best_bus_id = bus_id
    return wait_time * best_bus_id

def part2(entries: tuple) -> int:
    """part2 solver"""
    min_timestamp = 0
    moduli_product = 1
    for _, modulo in entries[1]:
        moduli_product *= modulo
    for remainder, modulo in entries[1]:
        ni = moduli_product // modulo
        modulo_inv = modinv(ni, modulo)
        min_timestamp += (remainder * ni * modulo_inv)
    return min_timestamp % moduli_product

def test_input_day_13():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 295
    assert part2(entries) == 1068781

def test_bench_day_13(benchmark):
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
