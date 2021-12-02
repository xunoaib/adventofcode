#!/usr/bin/env python3
import sys

def part1(lines):
    x, y = 0, 0
    for line in lines:
        move, amt = line.split()
        amt = int(amt)
        if move == 'forward':
            x += amt
        elif move == 'down':
            y += amt
        elif move == 'up':
            y -= amt
    return x * y

def part2(lines):
    x, y, aim = 0, 0, 0
    for line in lines:
        move, amt = line.split()
        amt = int(amt)
        if move == 'forward':
            x += amt
            y += aim * amt
        elif move == 'down':
            aim += amt
        elif move == 'up':
            aim -= amt
    return x * y

def main():
    lines = sys.stdin.readlines()
    ans1 = part1(lines)
    ans2 = part2(lines)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 1815044
    assert ans2 == 1739283308

if __name__ == "__main__":
    main()
