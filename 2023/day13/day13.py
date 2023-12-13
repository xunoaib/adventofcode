#!/usr/bin/env python3
import sys


def vdiffcount(lines, r):
    upper, lower = lines[:r][::-1], lines[r:]
    return sum(1 for a, b in zip(upper, lower) for x, y in zip(a, b) if x != y)


def vert(lines, diffcount):
    for r in range(1, len(lines)):
        if vdiffcount(lines, r) == diffcount:
            return r
    return 0


def horiz(lines, diffcount):
    return vert(list(zip(*lines)), diffcount)


def main():
    patterns = sys.stdin.read().strip().split('\n\n')
    a1 = a2 = 0

    for p in patterns:
        lines = p.split('\n')
        a1 += horiz(lines, 0) + vert(lines, 0) * 100
        a2 += horiz(lines, 1) + vert(lines, 1) * 100

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 35232
    assert a2 == 37982


if __name__ == '__main__':
    main()
