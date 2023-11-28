#!/usr/bin/env python
import sys

def part1(mass):
    return int(mass) // 3 - 2

def part2(mass):
    total = 0
    while (mass := part1(mass)) > 0:
        total += mass
    return total

def main():
    masses = list(map(int, sys.stdin))

    ans1 = sum(map(part1, masses))
    print('part1:', ans1)

    ans2 = sum(map(part2, masses))
    print('part2:', ans2)

    assert ans1 == 3434390
    assert ans2 == 5148724

if __name__ == '__main__':
    main()
