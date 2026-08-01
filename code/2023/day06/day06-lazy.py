#!/usr/bin/env python3
import re
import sys
from z3 import Int, Optimize


def solve(times, distances):
    ans = 1
    for time, dist in zip(times, distances):
        ways = 0
        for speed in range(1, time + 1):
            timeleft = time - speed
            if timeleft * speed > dist:
                ways += 1
        ans *= ways
    return ans


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
