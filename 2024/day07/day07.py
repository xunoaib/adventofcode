#!/usr/bin/env python3

import sys


def permute(nums, ops: str):
    if len(nums) == 1:
        yield nums[0]
        return

    for op in ops:
        a, b = nums[0:2]
        if op == '+':
            a += b
        elif op == '*':
            a *= b
        elif op == '|':
            a = int(f'{a}{b}')
        yield from permute((a, *nums[2:]), ops)

def find(tot, nums, operators):
    return next((v for v in permute(nums, operators) if v == tot), 0)

d = {}

for line in sys.stdin:
    a, b = line.strip().split(':')
    d[int(a)] = tuple(map(int, b.split()))

a1 = sum(find(tot, nums, '+*') for tot, nums in d.items())
print('part1:', a1)

a2 = sum(find(tot, nums, '+*|') for tot, nums in d.items())
print('part2:', a2)

assert a1 == 4998764814652
assert a2 == 37598910447546
