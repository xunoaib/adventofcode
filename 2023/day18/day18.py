#!/usr/bin/env python3
import re
import sys
from itertools import pairwise

DIRDICT = {'U': (-1, 0), 'L': (0, -1), 'R': (0, 1), 'D': (1, 0)}


def parseline1(line):
    dirch, count, _ = re.search(r'(.*) (.*) \(#(.*)\)', line).groups()
    roff, coff = DIRDICT[dirch]
    return roff, coff, int(count)


def parseline2(line):
    _, _, color = re.search(r'(.*) (.*) \(#(.*)\)', line).groups()
    roff, coff = DIRDICT['RDLU'[int(color[-1])]]
    return roff, coff, int(color[:-1], 16)


def solve(lines, parseline):
    r = c = 0
    points = [(r, c)]
    perimeter = 0

    for line in lines:
        roff, coff, count = parseline(line)
        r += roff * count
        c += coff * count
        points.append((r, c))
        perimeter += count

    # shoelace formula
    area = 0.5 * abs(
        sum((r1 + r2) * (c1 - c2) for (r1, c1), (r2, c2) in pairwise(points)))
    return int(area) + perimeter // 2 + 1


def main():
    lines = sys.stdin.read().strip().split('\n')

    a1 = solve(lines, parseline1)
    a2 = solve(lines, parseline2)

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 49578
    assert a2 == 52885384955882


if __name__ == '__main__':
    main()
