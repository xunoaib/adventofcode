#!/usr/bin/env python3

import sys
from itertools import product


def canmake(tot, nums, operators):
    allops = list(product(operators, repeat=len(nums)-1))

    for ops in allops:
        a = nums[0]
        for v,op in zip(nums[1:], ops):
            if op == '+':
                a += v
            elif op == '*':
                a *= v
            elif op == '|':
                a = int(f'{a}{v}')
        if a == tot:
            return tot
    return 0

d = {}

for line in sys.stdin:
    a, b = line.strip().split(':')
    d[int(a)] = list(map(int, b.split()))

a1 = sum(canmake(tot, nums, '+*') for tot, nums in d.items())
print('part1:', a1)

a2 = sum(canmake(tot, nums, '+*|') for tot, nums in d.items())
print('part2:', a2)

assert a1 == 4998764814652
assert a2 == 37598910447546
