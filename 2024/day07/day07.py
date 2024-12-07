#!/usr/bin/env python3

import sys
from itertools import product


def canmake(tot, nums):
    allops = list(product('+*', repeat=len(nums)-1))

    for ops in allops:
        a = nums[0]
        for v,op in zip(nums[1:], ops):
            if op == '+':
                a += v
            else:
                a *= v
        if a == tot:
            return True
    return False

d = {}

for line in sys.stdin:
    a, b = line.strip().split(':')
    d[int(a)] = list(map(int, b.split()))

a = 0
for tot, nums in d.items():
    if canmake(tot, nums):
        print('YES', tot, nums)
        a += tot
    else:
        print('NO ', tot, nums)

print('part1:', a)
