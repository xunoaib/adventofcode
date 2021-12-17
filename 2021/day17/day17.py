#!/usr/bin/env python3
import re
import sys
from itertools import count, product


def valid_yvel(vel, ymin, ymax):
    y = 0
    while y >= ymin:
        y += vel
        vel -= 1
        if ymin <= y <= ymax:
            return True
    return False


def valid_velocity(xvel, yvel, xmin, xmax, ymin, ymax):
    for step in count(0):
        x, y = getpos(xvel, yvel, step)
        if x > xmax or y < ymin:
            return False
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return True


def getpos(xvel, yvel, step):
    x, y = 0, 0
    for i in range(step):
        x += xvel
        y += yvel
        if xvel > 0:
            xvel -= 1
        yvel -= 1
    return x, y


def part1(xmin, xmax, ymin, ymax):
    yvels = find_yvels(xmin, xmax, ymin, ymax)
    return sum(range(yvels[-1] + 1))


def find_yvels(xmin, xmax, ymin, ymax):
    yvels = []
    for vel_y in count(ymin):
        if valid_yvel(vel_y, ymin, ymax):
            yvels.append(vel_y)
        if vel_y > 100:  # horribly hardcoded
            return yvels


def part2(xmin, xmax, ymin, ymax):
    vx_min = next(vx for vx in count(0) if sum(range(vx + 1)) > xmin)
    vx_max = xmax

    yvels = find_yvels(xmin, xmax, ymin, ymax)
    vy_min, vy_max = yvels[0], yvels[-1]

    valid = set()
    for xvel, yvel in product(range(vx_min, vx_max + 1),
                              range(vy_min, vy_max + 1)):
        if valid_velocity(xvel, yvel, xmin, xmax, ymin, ymax):
            valid.add((xvel, yvel))

    return len(valid)


def main():
    match = re.search(r' x=(.*)\.\.(.*), y=(.*)\.\.(.*)', sys.stdin.read())
    xmin, xmax, ymin, ymax = map(int, match.groups())

    ans1 = part1(xmin, xmax, ymin, ymax)
    print('part1:', ans1)

    ans2 = part2(xmin, xmax, ymin, ymax)
    print('part2:', ans2)

    assert ans1 == 4095
    assert ans2 == 3773


if __name__ == '__main__':
    main()
