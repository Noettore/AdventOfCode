"""AOC 2020 Day 14"""

import pathlib
import time
import re
import itertools

TEST_INPUT = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

TEST_INPUT_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> list:
    """take input data and return the appropriate data structure"""
    entries = list()
    mem_rexp = re.compile(r'mem\[(\d+)\] = (\d+)')
    for line in input_data.split('\n'):
        if line.startswith('mask'):
            entry = {
                'type': 'mask',
                'value': line[7:].rstrip(),
            }
        else:
            entry = {
                'type': 'mem',
                'value': mem_rexp.match(line).groups(),
            }
        entries.append(entry)
    return entries

def generate_addresses(addr: str, mask: str) -> list:
    """generate all possible addresses from floating mask"""
    generator_bits = list()
    addresses = list()
    addr = format(int(addr), '036b')
    for addr_bit, mask_bit in zip(addr, mask):
        if mask_bit == '0':
            generator_bits.append(addr_bit)
        elif mask_bit == '1':
            generator_bits.append('1')
        else:
            generator_bits.append('01')
    for address in itertools.product(*generator_bits):
        addresses.append(int(''.join(address), 2))
    return addresses

def part1(entries: dict) -> int:
    """part1 solver"""
    mem = dict()
    mask_set0s = 0
    mask_set1s = 0
    for entry in entries:
        if entry['type'] == 'mask':
            mask = entry['value']
            mask_set0s = int(mask.replace('X', '1'), 2)
            mask_set1s = int(mask.replace('X', '0'), 2)
        else:
            addr, value = entry['value']
            mem[addr] = (int(value) & mask_set0s) | mask_set1s
    return sum(mem.values())

def part2(entries: tuple) -> int:
    """part2 solver"""
    mem = dict()
    mask = ''
    for entry in entries:
        if entry['type'] == 'mask':
            mask = entry['value']
        else:
            addr, value = entry['value']
            for address in generate_addresses(addr, mask):
                mem[address] = int(value)
    return sum(mem.values())

def test_input_day_14():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 165
    entries = extract(TEST_INPUT_2)
    assert part2(entries) == 208

def test_bench_day_14(benchmark):
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
