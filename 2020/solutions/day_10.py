"""AOC 2020 Day 10"""

import pathlib
import time

TEST_INPUT = """16
10
15
5
1
11
7
19
6
12
4"""

TEST_INPUT_2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = [0]
    for entry in input_data.split('\n'):
        entries.append(int(entry))
    entries = sorted(entries)
    entries.append(entries[-1]+3)
    return entries

def part1(entries: list) -> int:
    """part1 solver"""
    jolt_diff_1, jolt_diff_3 = 0, 0
    for index in range(len(entries)-1):
        diff = entries[index+1] - entries[index]
        if diff == 1:
            jolt_diff_1 += 1
        elif diff == 3:
            jolt_diff_3 += 1
    return jolt_diff_1*jolt_diff_3

def part2(entries: list) -> int:
    """part2 solver"""
    distinct_paths = [0]*(entries[-1]+1)
    distinct_paths[0] = 1

    for adapter in entries:
        distinct_paths[adapter] += distinct_paths[adapter-1] + distinct_paths[adapter-2] + distinct_paths[adapter-3]

    return distinct_paths[len(distinct_paths)-1]

def test_input_day_10():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 35
    assert part2(entries) == 8
    entries = extract(TEST_INPUT_2)
    assert part1(entries) == 220
    assert part2(entries) == 19208

def test_bench_day_10(benchmark):
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
