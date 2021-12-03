"""AOC Day 3"""

from os import read
import pathlib
import time

TEST_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    return input_data.split('\n')

def common_bits(lines: list) -> list:
    """common_bits take a list of strings representing binary numbers and return a list of int one per digit. Each int can be 0, > 0 or < 0 if the number of 1s and 0s in that column are equal, more 1s or more 0s"""
    col_num = len(lines[0])
    columns = [0]*col_num
    for line in lines:
        bits = list(map(int, line))
        for i, b in enumerate(bits):
            if b == 0:
                columns[i] -= 1
            elif b == 1:
                columns[i] += 1
    return columns

def common_bit(lines: list, column_number: int) -> int:
    """common_bits take a list of strings representing binary numbers and a column number and return an int that can be 0, > 0 or < 0 if the number of 1s and 0s in that column are equal, more 1s or more 0s"""
    cb = 0
    for line in lines:
        bits = list(map(int, line))
        if bits[column_number] == 0:
            cb -= 1
        elif cb == 1:
            cb += 1
    return cb

def part1(entries: list) -> int:
    """part1 solver take the entries and return the part1 solution"""
    gamma_rate = ''
    epsilon_rate = ''
    columns = common_bits(entries)

    for common_bit in columns:
        if common_bit > 0:
            gamma_rate += '1'
            epsilon_rate += '0'
        elif common_bit < 0:
            gamma_rate += '0'
            epsilon_rate += '1'
    
    return int(gamma_rate, 2)*int(epsilon_rate, 2)

def part2(entries: list) -> int:
    """part2 solver take the entries and return the part2 solution"""
    og_rating = ''
    co2s_rating = ''

    nums = entries.copy()
    i = 0
    while len(nums) > 1:
        cb = common_bit(nums, i)
        new_nums = list()
        for num in nums:
            if cb >= 0 and num[i] == '1':
                new_nums.append(num)
            elif cb < 0 and num[i] == '0':
                new_nums.append(num)
        nums = new_nums.copy()
        i += 1
    og_rating = nums[0]

    nums = entries.copy()
    i = 0
    while len(nums) > 1:
        cb = common_bit(nums, i)
        new_nums = list()
        for num in nums:
            if cb >= 0 and num[i] == '0':
                new_nums.append(num)
            elif cb < 0 and num[i] == '1':
                new_nums.append(num)
        nums = new_nums.copy()
        i += 1
    co2s_rating = nums[0]

    return int(og_rating, 2)*int(co2s_rating, 2)

def test_input_day_03():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 198
    assert part2(entries) == 230

def test_bench_day_03(benchmark):
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