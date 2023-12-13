#!/usr/bin/env python3
import sys


def vdiffcount(lines, r):
    upper, lower = lines[:r][::-1], lines[r:]
    return sum(1 for a, b in zip(upper, lower) for x, y in zip(a, b) if x != y)


def findvert(lines, diffcount):
    for r in range(1, len(lines)):
        if vdiffcount(lines, r) == diffcount:
            return r
    return 0


def findhoriz(lines, diffcount):
    lines = [''.join(line[c] for line in lines) for c in range(len(lines[0]))]
    return findvert(lines, diffcount)


def main():
    patterns = sys.stdin.read().strip().split('\n\n')
    a1 = a2 = 0

    for p in patterns:
        lines = p.split('\n')
        a1 += findhoriz(lines, 0) + findvert(lines, 0) * 100
        a2 += findhoriz(lines, 1) + findvert(lines, 1) * 100

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 35232
    assert a2 == 37982


if __name__ == '__main__':
    main()
