#!/usr/bin/env python3
import sys

def count_bits(lines):
    d = [0] * len(lines[0])
    for line in lines:
        for idx, bit in enumerate(line):
            if bit == '1':
                d[int(idx)] += 1
    return d

def part1(lines):
    d = count_bits(lines)

    gamma = ''
    for idx, ones in sorted(enumerate(d)):
        gamma += '1' if ones > len(lines)/2 else '0'

    gamma = int(gamma, 2)
    epsilon = 2 ** len(lines[0])-1 - gamma
    return gamma * epsilon

def remove_lines(lines, idx, keep_bit):
    return [line for line in lines if line[idx] == keep_bit]

def calc_oxy(lines):
    d = count_bits(lines)
    for idx in range(len(d)):
        keep_bit = '1' if d[idx] >= len(lines)/2 else '0'
        lines = remove_lines(lines, idx, keep_bit)
        d = count_bits(lines)
        if len(lines) <= 1:
            break
    return int(lines[0], 2)

def calc_co2(lines):
    d = count_bits(lines)
    for idx in range(len(d)):
        keep_bit = '1' if d[idx] < len(lines)/2 else '0'
        lines = remove_lines(lines, idx, keep_bit)
        d = count_bits(lines)
        if len(lines) <= 1:
            break
    return int(lines[0], 2)

def part2(lines):
    oxy = calc_oxy(lines)
    co2 = calc_co2(lines)
    return oxy * co2

def main():
    lines = sys.stdin.read().strip().split('\n')
    ans1 = part1(lines)
    ans2 = part2(lines)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 3923414
    assert ans2 == 5852595

if __name__ == "__main__":
    main()
