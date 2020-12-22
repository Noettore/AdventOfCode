"""AOC 2020 Day 22"""

import pathlib
import time
import collections
import itertools

TEST_INPUT = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    deck1, deck2 = input_data.split('\n\n')
    deck1, deck2 = deck1.splitlines(), deck2.splitlines()
    deck1 = collections.deque(map(int, deck1[1:]))
    deck2 = collections.deque(map(int, deck2[1:]))

    return deck1, deck2

def play_space_cards(deck1: collections.deque, deck2: collections.deque) -> collections.deque:
    """return the winner's deck after a space cards game"""
    assert len(deck1) == len(deck2)
    while deck1 and deck2:
        card1, card2 = deck1.popleft(), deck2.popleft()
        assert card1 != card2
        if card1 > card2:
            deck1.extend((card1, card2))
        else:
            deck2.extend((card2, card1))

    return deck1 if deck1 else deck2

def play_recursive_space_cards(deck1: collections.deque, deck2: collections.deque) -> tuple:
    """return the winner and its deck after a recursive space cards game"""
    configurations = set()

    while deck1 and deck2:
        current_config = (tuple(deck1), tuple(deck2))
        if current_config in configurations:
            return 1, deck1
        configurations.add(current_config)

        card1, card2 = deck1.popleft(), deck2.popleft()
        assert card1 != card2
        if card1 <= len(deck1) and card2 <= len(deck2):
            sub_deck1 = collections.deque(itertools.islice(deck1, card1))
            sub_deck2 = collections.deque(itertools.islice(deck2, card2))
            winner, _ = play_recursive_space_cards(sub_deck1, sub_deck2)
        else:
            winner = 1 if card1 > card2 else 2

        if winner == 1:
            deck1.extend((card1, card2))
        else:
            deck2.extend((card2, card1))

    return (1, deck1) if deck1 else (2, deck2)

def part1(entries: tuple) -> int:
    """part1 solver"""
    deck1, deck2 = entries[0].copy(), entries[1].copy()
    winner = play_space_cards(deck1, deck2)
    return sum(index * card for index, card in enumerate(reversed(winner), 1))

def part2(entries: tuple) -> str:
    """part2 solver"""
    deck1, deck2 = entries
    _, winner = play_recursive_space_cards(deck1, deck2)
    return sum(index * card for index, card in enumerate(reversed(winner), 1))

def test_input_day_22():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 306
    assert part2(entries) == 291

def test_bench_day_22(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    print("Part 1: %d" % part1(entries))
    print("Part 2: %s" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
