#!/usr/bin/env python3
import re
import sys

from z3 import Int, If, Solver

CHECK_Y = 2000000
MAX_COORD = 4000000


def manhattan_dist(src, tar):
    x1, y1 = src
    x2, y2 = tar
    return abs(x1 - x2) + abs(y1 - y2)


def z3abs(x):
    return If(x >= 0, x, -x)


def main():
    lines = sys.stdin.read().strip().split('\n')
    sensors = set()
    beacons = set()
    invalid = set()

    sensor_ranges = {}

    for line in lines:
        match = re.match( r'Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)$', line)
        sx, sy, bx, by = map(int, match.groups())
        beacons.add((bx, by))
        sensors.add((sx, sy))

        max_range = manhattan_dist((sx, sy), (bx, by))
        dist_to_row = abs(sy - CHECK_Y)
        dist_diff = max_range - dist_to_row

        if dist_diff >= 0:
            numvals = dist_diff * 2 + 1
            invalid |= {sx + x - dist_diff for x in range(numvals)}

        sensor_ranges[(sx, sy)] = max_range

    invalid -= set(x for x, y in beacons if y == CHECK_Y)
    ans1 = len(invalid)
    print('part1:', ans1)

    x = Int('x')
    y = Int('y')

    solver = Solver()
    solver.add(x >= 0)
    solver.add(y >= 0)
    solver.add(x <= MAX_COORD)
    solver.add(y <= MAX_COORD)

    for (sx, sy), maxrange in sensor_ranges.items():
        solver.add(z3abs(x - sx) + z3abs(y - sy) > maxrange)

    solver.check()
    model = solver.model()
    ans2 = model[x].as_long() * 4000000 + model[y].as_long()
    print('part2:', ans2)

    assert ans1 == 5508234
    assert ans2 == 10457634860779


if __name__ == '__main__':
    main()
