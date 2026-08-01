#!/usr/bin/env python3
from collections import Counter
import sys

def part1(data, houses=None):
    if houses is None:
        houses = Counter()

    x,y = 0,0
    for ch in data:
        if ch == '>':
            x += 1
        elif ch == '<':
            x -= 1
        elif ch == '^':
            y += 1
        elif ch == 'v':
            y -= 1
        houses[(x,y)] += 1
    return len(houses)

def part2(data):
    houses = Counter()
    part1(data[::2], houses)
    part1(data[1::2], houses)
    return len(houses)

def main():
    data = sys.stdin.read().strip()

    ans1 = part1(data)
    print('part1:', ans1)

    ans2 = part2(data)
    print('part2:', ans2)

    assert ans1 == 2565
    assert ans2 == 2639

if __name__ == '__main__':
    main()
