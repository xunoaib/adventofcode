#!/usr/bin/env python3

import sys
from functools import cache


@cache
def count_ways(s):
    return sum(count_ways(s[len(a):]) for a in avail if s.startswith(a)) if s else 1

a,b = sys.stdin.read().strip().split('\n\n')
avail = set(a.split(', '))
designs = b.split('\n')

counts = list(map(count_ways, designs))

a1 = sum(c > 0 for c in counts)
a2 = sum(counts)

print('part1:', a1)
print('part2:', a2)

assert a1 == 363
assert a2 == 642535800868438
