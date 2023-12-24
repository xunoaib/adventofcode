#!/usr/bin/env python3
import re
import sys
from itertools import combinations


def main():
    lines = sys.stdin.read().strip().split('\n')

    stones = []
    for line in lines:
        if m := re.match(r'(\d+), (\d+), (\d+) @ (.*), (.*), (.*)', line):
            stones.append(list(map(int, m.groups())))

    coeffs = []
    for stone in stones:
        px, py, pz, vx, vy, vz = stone
        m = vy / vx
        b = py - m * px
        coeff = A, B, C = (m, -1, b)
        coeffs.append(coeff)

    # vmin, vmax = (7, 27)
    vmin, vmax = (200000000000000, 400000000000000)

    crossed = set()
    for (idx_a, coeffs_a), (idx_b, coeffs_b) in combinations(enumerate(coeffs),
                                                             r=2):
        a1, b1, c1 = coeffs_a
        a2, b2, c2 = coeffs_b
        try:
            xint = (c2 - c1) / (a1 - a2)
            yint = a1 * (c2 - c1) / (a1 - a2) + c1

            # ensure the collision happens in the future
            px_a, _, _, vx_a, _, _ = stones[idx_a]
            px_b, _, _, vx_b, _, _ = stones[idx_b]
            t_a = (xint - px_a) / vx_a
            t_b = (xint - px_b) / vx_b
            if t_a < 0 or t_b < 0:
                continue

            if vmin <= xint <= vmax and vmin <= yint <= vmax:
                crossed |= {(idx_a, idx_b)}

        except ZeroDivisionError:
            pass  # no intersection

    a1 = len(crossed)
    print('part1:', )

    assert a1 == 16665


if __name__ == '__main__':
    main()
