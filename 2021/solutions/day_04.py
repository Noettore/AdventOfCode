"""AOC Day 4"""

from os import read
import pathlib
import time

TEST_INPUT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    matrixs = input_data.split('\n\n')
    drawn_nums = list(map(int, matrixs.pop(0).split(',')))
    cards = list()
    for matrix in matrixs:
        card = []
        for line in matrix.split('\n'):
            card.append(list(map(int, line.split())))
        cards.append(card)
    return (drawn_nums, cards)

def check_card(card: list, r: int, c: int) -> bool:
    if sum(x == -1 for x in card[r]) == 5:
        return True
    if sum(row[c] == -1 for row in card) == 5:
        return True
    return False

def mark_num(card: list, num: int) -> bool:
    for row_num, row in enumerate(card):
        for col_num, cell in enumerate(row):
            if cell == num:
                card[row_num][col_num] = -1
                return check_card(card, row_num, col_num)
    return False

def card_score(card: list, last_num: int) -> int:
    unmarked_sum = 0
    for row in card:
        for cell in row:
            if cell != -1:
                unmarked_sum += cell
    return unmarked_sum*last_num

def part1and2(entries: tuple) -> tuple:
    """part2 solver take the entries and return the part2 solution"""
    drawn_nums, cards = entries
    n_cards = len(cards)
    won_cards = 0

    first_score = 0
    last_score = 0

    for num in drawn_nums:
        for i, card in enumerate(cards):
            if card is None:
                continue
            if mark_num(card, num):
                won_cards += 1
                if won_cards == 1:
                    first_score = card_score(card, num)
                if won_cards == n_cards:
                    last_score = card_score(card, num)
                cards[i] = None
    
    return (first_score, last_score)

def test_input_day_04():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    p1, p2 = part1and2(entries)
    assert p1 == 4512
    assert p2 == 1924

def test_bench_day_04(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    p1, p2 = part1and2(entries)
    print("Part 1: %d" % p1)
    print("Part 2: %d" % p2)
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
