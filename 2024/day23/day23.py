#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import combinations

lines = sys.stdin.read().strip().split('\n')

g = defaultdict(set)

for line in lines:
    a,b = line.split('-')
    g[a].add(b)
    g[b].add(a)

a1 = 0
for p in combinations(g, r=3):
    if not any(c.startswith('t') for c in p):
        continue

    a,b,c = p
    sa = {a} | g[a]
    sb = {b} | g[b]
    sc = {c} | g[c]

    if set(p).issubset(sa & sb & sc):
        a1 += 1

print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
