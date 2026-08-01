#!/usr/bin/env python3
import re
import sys
from itertools import count, product


def hits_target(xvel, yvel, xmin, xmax, ymin, ymax):
    """Checks if the launch vector lands in the target region"""
    for t in count(0):
        x, y = getpos(xvel, yvel, t)
        if x > xmax or y < ymin:
            return False
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return True


def getpos(xvel, yvel, t):
    """Calculate the (x,y) position after 't' steps given a launch vector"""
    x, y = 0, 0
    for _ in range(t):
        x += xvel
        y += yvel
        if xvel > 0:
            xvel -= 1
        yvel -= 1
    return x, y


def part2(xmin, xmax, ymin, ymax):
    vx_min = next(vx for vx in count(0) if sum(range(vx + 1)) > xmin)
    vy_range = max(abs(ymin), abs(ymax))

    vectors = set()
    for xvel, yvel in product(range(vx_min, xmax + 1),
                              range(-vy_range, vy_range + 1)):
        if hits_target(xvel, yvel, xmin, xmax, ymin, ymax):
            vectors.add((xvel, yvel))

    return len(vectors)


def main():
    match = re.search(r' x=(.*)\.\.(.*), y=(.*)\.\.(.*)', sys.stdin.read())
    xmin, xmax, ymin, ymax = map(int, match.groups())

    ans1 = sum(range(abs(ymin)))
    print('part1:', ans1)

    ans2 = part2(xmin, xmax, ymin, ymax)
    print('part2:', ans2)

    assert ans1 == 4095
    assert ans2 == 3773


if __name__ == '__main__':
    main()
