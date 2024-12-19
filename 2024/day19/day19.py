#!/usr/bin/env python3

import sys
from functools import cache

a,b = sys.stdin.read().strip().split('\n\n')

avails = set(a.split(', '))
designs = b.split('\n')

@cache
def count_ways(s):
    if s == '':
        return 1
    tot = 0
    for a in avails:
        if s.startswith(a):
            tot += count_ways(s[len(a):])
    return tot

counts = list(map(count_ways, designs))

a1 = sum([c > 0 for c in counts])
a2 = sum(counts)

print('part1:', a1)
print('part2:', a2)

assert a1 == 363
assert a2 == 642535800868438
