#!/usr/bin/env python3
import math
import re
import sys


def solve(times, distances):
    ans = 1
    for time, dist in zip(times, distances):
        low, high = sorted(quadratic(-1, time, -dist))
        if low - int(low) < 0.0001:
            low += 0.0001
        if high - int(high) < 0.0001:
            high -= 0.0001
        ans *= math.floor(high) - math.ceil(low) + 1
    return ans


def quadratic(a, b, c):
    x1 = (-b + math.sqrt((b**2) - (4 * (a * c)))) / (2 * a)
    x2 = (-b - math.sqrt((b**2) - (4 * (a * c)))) / (2 * a)
    return x1, x2


def main():
    lines = sys.stdin.read().strip().split('\n')

    times, distances = [
        list(map(int, re.findall(r'\d+', line))) for line in lines
    ]

    time2 = int(''.join(map(str, times)))
    dist2 = int(''.join(map(str, distances)))

    ans1 = solve(times, distances)
    ans2 = solve([time2], [dist2])

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 2756160
    assert ans2 == 34788142


if __name__ == '__main__':
    main()
