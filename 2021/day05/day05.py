#!/usr/bin/env python3
import re
import sys
from collections import defaultdict

def gen_points(x1, y1, x2, y2):
    """Generate all points between (x1, y1) and (x2, y2), orthogonally and/or diagonally"""
    xoff, yoff = 0, 0
    if x1 != x2:
        xoff = 1 if x1 < x2 else -1
    if y1 != y2:
        yoff = 1 if y1 < y2 else -1

    while (x1, y1) != (x2, y2):
        yield x1, y1
        x1 += xoff
        y1 += yoff
    yield x2, y2

def part1(lines):
    """Count the number of points where at least 2 lines intersect (excluding diagonals)"""
    d = defaultdict(lambda: 0)
    for pts in lines:
        if pts[0] == pts[2] or pts[1] == pts[3]:  # ignore diagonals
            for pt in gen_points(*pts):
                d[pt] += 1
    return sum(1 for n in d.values() if n > 1)

def part2(lines):
    """Count the number of points where at least 2 lines intersect"""
    d = defaultdict(lambda: 0)
    for pts in lines:
        for pt in gen_points(*pts):
            d[pt] += 1
    return sum(1 for n in d.values() if n > 1)

def main():
    lines = [list(map(int, re.split(r',| -> ', line))) for line in sys.stdin]

    ans1 = part1(lines)
    ans2 = part2(lines)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 5774
    assert ans2 == 18423

if __name__ == '__main__':
    main()
