#!/usr/bin/env python3

import sys
from itertools import pairwise


def isgood(nums):
    diffs = [a-b for a,b in pairwise(nums)]

    inc = all(x > 0 for x in diffs)
    dec = all(x < 0 for x in diffs)
    amt = all(1 <= abs(x) <= 3 for x in diffs)

    return (inc or dec) and amt

p1 = p2 = 0

for line in sys.stdin:
    nums = list(map(int, line.split()))

    if isgood(nums):
        p1 += 1

    for i in range(len(nums)):
        n = nums[:i] + nums[i+1:]
        if isgood(n):
            p2 += 1
            break

print('part1:', p1)
print('part2:', p2)
