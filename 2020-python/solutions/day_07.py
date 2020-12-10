"""AOC Day 6"""

import pathlib
import time
import collections

TEST_INPUT = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

TEST_INPUT_2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    rules = input_data.split('\n')
    graph = dict()
    reverse_graph = dict()
    for rule in rules:
        container, contents = rule.split('contain')
        container = ' '.join(container.split()[:2])
        content_graph = dict()
        for content in contents.split(','):
            if content == " no other bags.":
                break
            parts = content.split()
            amount = int(parts[0])
            color = ' '.join(parts[1:3])
            content_graph[color] = amount

            if color in reverse_graph.keys():
                reverse_graph[color].append(container)
            else:
                reverse_graph[color] = [container]
        graph[container] = content_graph
    return (graph, reverse_graph)

def part1(reverse_graph: dict, color: str) -> int:
    """part1 solver take a dict of lists and return an int"""
    queue = collections.deque(reverse_graph[color])
    already_counted = set()
    while queue:
        container = queue.popleft()
        if container not in already_counted:
            already_counted.add(container)
            if container in reverse_graph.keys():
                queue += collections.deque(reverse_graph[container])
    return len(already_counted)

def part2(graph: dict, color: str) -> int:
    """part2 solver take a dict of dicts and return an int"""
    def search_count(graph: dict, color: str) -> int:
        if not graph[color]:
            return 1
        count = 1
        for content, amount in graph[color].items():
            count += amount * search_count(graph, content)
        return count
    return search_count(graph, color)-1

def test_input_day_7():
    """pytest testing function"""
    graph, reverse_graph = extract(TEST_INPUT)
    assert part1(reverse_graph, "shiny gold") == 4
    assert part2(graph, "shiny gold") == 32

    graph, _ = extract(TEST_INPUT_2)
    assert part2(graph, "shiny gold") == 126

def test_bench_day_7(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    graph, reverse_graph = extract(input_data)
    print("Part 1: %d" % part1(reverse_graph, "shiny gold"))
    print("Part 2: %d" % part2(graph, "shiny gold"))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
