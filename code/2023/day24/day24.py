#!/usr/bin/env python3
import re
import sys
from itertools import combinations

from z3 import Real, Reals, Solver, sat

VMIN, VMAX = (200000000000000, 400000000000000)


def part1(stones):
    coeffs = []  # ax + bx + c
    for stone in stones:
        px, py, pz, vx, vy, vz = stone
        m = vy / vx
        b = py - m * px
        coeffs.append((m, -1, b))

    crossed = set()
    for (idx_a, coeffs_a), (idx_b, coeffs_b) in combinations(enumerate(coeffs),
                                                             r=2):
        a1, b1, c1 = coeffs_a
        a2, b2, c2 = coeffs_b
        try:
            xint = (c2 - c1) / (a1 - a2)
            yint = a1 * (c2 - c1) / (a1 - a2) + c1

            # ensure the collision happens in the future
            px_a, py_a, pz_a, vx_a, vy_a, vz_a = stones[idx_a]
            px_b, py_b, pz_b, vx_b, vy_b, vz_b = stones[idx_b]
            t_a = (xint - px_a) / vx_a
            t_b = (xint - px_b) / vx_b

            if t_a < 0 or t_b < 0:
                continue

            if VMIN <= xint <= VMAX and VMIN <= yint <= VMAX:
                crossed |= {(idx_a, idx_b)}

        except ZeroDivisionError:
            pass  # parallel

    return len(crossed)


def part2(stones):
    s = Solver()
    gpx, gpy, gpz, gvx, gvy, gvz = Reals('gpx gpy gpz gvx gvy gvz')

    for i, stone in enumerate(stones):
        px, py, pz, vx, vy, vz = stone
        t = Real(f't{i}')
        s.add(gpx + t * gvx == px + t * vx)
        s.add(gpy + t * gvy == py + t * vy)
        s.add(gpz + t * gvz == pz + t * vz)

    assert s.check() == sat
    m = s.model()
    return m.eval(gpx + gpy + gpz)


def main():
    lines = sys.stdin.read().strip().split('\n')

    stones = []
    for line in lines:
        if m := re.match(r'(\d+), (\d+), (\d+) @ (.*), (.*), (.*)', line):
            stones.append(list(map(int, m.groups())))

    a1 = part1(stones)
    print('part1:', a1)

    a2 = part2(stones)
    print('part2:', a2)

    assert a1 == 16665
    assert a2 == 769840447420960


if __name__ == '__main__':
    main()
