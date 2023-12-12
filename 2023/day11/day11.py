#!/usr/bin/env python3
import sys
from itertools import combinations


def solve(lines, expand_multiplier):
    erows = [r for r, line in enumerate(lines) if set(line) == {'.'}]
    ecols = [
        c for c, _ in enumerate(lines[0])
        if set(line[c] for line in lines) == {'.'}
    ]

    galaxies = sorted((r, c) for r, line in enumerate(lines)
                      for c, ch in enumerate(line) if ch == '#')

    adds = [[0, 0] for _ in galaxies]

    for i, (r, c) in enumerate(galaxies):
        adds[i][0] += sum(expand_multiplier - 1 for erow in erows if erow < r)
        adds[i][1] += sum(expand_multiplier - 1 for ecol in ecols if ecol < c)

    for i, (gr, gc) in enumerate(galaxies):
        galaxies[i] = (gr + adds[i][0], gc + adds[i][1])

    return sum(
        abs(a[0] - b[0]) + abs(a[1] - b[1])
        for a, b in combinations(galaxies, 2))


def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = solve(lines, 2)
    ans2 = solve(lines, 1_000_000)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 9769724
    assert ans2 == 603020563700


if __name__ == '__main__':
    main()
