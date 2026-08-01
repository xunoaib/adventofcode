#!/usr/bin/env python3
import sys
from itertools import pairwise


def solve(row):
    s = [row]
    while len(set(row)) > 1:
        row = [b - a for a, b in pairwise(row)]
        s.append(row)
    return sum(r[-1] for r in s)


def main():
    lines = sys.stdin.read().strip().split('\n')
    nums = [list(map(int, line.split(' '))) for line in lines]

    ans1 = sum(map(solve, nums))
    ans2 = sum(solve(r[::-1]) for r in nums)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 1868368343
    assert ans2 == 1022


if __name__ == '__main__':
    main()
