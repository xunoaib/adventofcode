#!/usr/bin/env python3
import sys

def count_column(lines, column_idx):
    ''' Count the number of 1s in a specific column '''
    return sum(int(line[column_idx]) for line in lines)

def count_columns(lines):
    ''' Count the number of 1s in each column '''
    return [count_column(lines, cidx) for cidx in range(len(lines[0]))]

def part1(lines):
    counts = count_columns(lines)
    gamma = ''.join('1' if ones > len(lines)/2 else '0' for ones in counts)
    gamma = int(gamma, 2)
    epsilon = 2 ** len(lines[0])-1 - gamma  # bitwise NOT of gamma
    return gamma * epsilon

def remove_lines(lines, column_idx, keep_bit):
    ''' Remove lines that do not have a matching bit value in the given column '''
    return [line for line in lines if int(line[column_idx]) == int(keep_bit)]

def sieve(lines, keep_common: bool):
    ''' Iteratively remove lines that do not contain the most common bit in each column.
        If keep_common is False, remove lines that contain the LEAST common bit.
        Returns: numeric representation of the remaining line
    '''
    bitcounts = count_columns(lines)
    for idx in range(len(bitcounts)):
        keep_bit = int((bitcounts[idx] >= len(lines)/2) == keep_common)
        lines = remove_lines(lines, idx, keep_bit)
        bitcounts = count_columns(lines)
        if len(lines) == 1:
            return int(lines[0], 2)

def part2(lines):
    oxy = sieve(lines, True)
    co2 = sieve(lines, False)
    return oxy * co2

def main():
    lines = sys.stdin.read().split()

    ans1 = part1(lines)
    ans2 = part2(lines)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 3923414
    assert ans2 == 5852595

if __name__ == '__main__':
    main()
