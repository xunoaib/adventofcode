#!/usr/bin/env python3
import sys

def part1(data):
    return data.count('(') - data.count(')')

def part2(data):
    level = 0
    for idx, ch in enumerate(data):
        if ch == '(':
            level += 1
        else:
            level -= 1
        if level == -1:
            return idx + 1

def main():
    data = sys.stdin.read().strip()

    ans1 = part1(data)
    print('part1:', ans1)

    ans2 = part2(data)
    print('part2:', ans2)

    assert ans1 == 232
    assert ans2 == 1783

if __name__ == '__main__':
    main()
