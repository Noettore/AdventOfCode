"""AOC Day 12"""

import pathlib
import time
from collections import defaultdict, deque

TEST_INPUT_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

TEST_INPUT_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

TEST_INPUT_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> defaultdict:
    """take input data and return the appropriate data structure"""
    graph = defaultdict(list)
    entries = input_data.split('\n')
    for entry in entries:
        a, b = entry.split('-')
        if b != 'start':
            graph[a].append(b)
        if a != 'start':
            graph[b].append(a) 
    return graph

def count_paths_1(graph: defaultdict, src: str, dst: str) -> int:
    stack = deque([(src, {src})])
    total = 0

    while stack:
        node, visited = stack.pop()
        if node == dst:
            total += 1
            continue

        for n in graph[node]:
            if n in visited and n.islower():
                continue
            stack.append((n, visited | {n}))

    return total

def count_paths_2(graph: defaultdict, src: str, dst: str) -> int:
    stack = deque([(src, {src}, False)])
    total = 0

    while stack:
        node, visited, double = stack.pop()
        if node == dst:
            total += 1
            continue

        for n in graph[node]:
            if n not in visited or n.isupper():
                stack.append((n, visited | {n}, double))
                continue
            if double:
                continue
            stack.append((n, visited, True))

    return total

def part1(graph: defaultdict) -> int:
    """part1 solver take the entries and return the part1 solution"""
    return count_paths_1(graph, 'start', 'end')

def part2(graph: defaultdict) -> int:
    """part2 solver take the entries and return the part2 solution"""
    return count_paths_2(graph, 'start', 'end')

def test_input_day_12():
    """pytest testing function"""
    entries_1 = extract(TEST_INPUT_1)
    entries_2 = extract(TEST_INPUT_2)
    entries_3 = extract(TEST_INPUT_3)

    assert part1(entries_1) == 10
    assert part1(entries_2) == 19
    assert part1(entries_3) == 226

    assert part2(entries_1) == 36
    assert part2(entries_2) == 103
    assert part2(entries_3) == 3509


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
