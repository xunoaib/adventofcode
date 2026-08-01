#!/usr/bin/env python3
from collections import Counter
from functools import cache


@cache
def split(num, d):
    if d == 0:
        return 1
    if num == 0:
        return split(1, d-1)
    elif len(str(num)) % 2 == 0:
        s = str(num)
        left, right = [int(s[:len(s)//2]), int(s[len(s)//2:])]
        return split(left, d-1) + split(right, d-1)
    return split(num * 2024, d-1)

counts = Counter(tuple(map(int, input().split())))

a1 = sum(count * split(n, 25) for n, count in counts.items())
a2 = sum(count * split(n, 75) for n, count in counts.items())

print('part1:', a1)
print('part2:', a2)

assert a1 == 203953
assert a2 == 242090118578155
