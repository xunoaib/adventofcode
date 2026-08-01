#!/usr/bin/env python3

import re
import sys
from collections import defaultdict

lines = sys.stdin.read().strip().split('\n')

counts = defaultdict(set)
intersecting = defaultdict(set)

for line in lines:
    if m := re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line):
        n, l, t, w, h = map(int, m.groups())
        for x in range(l, l + w):
            for y in range(t, t + h):
                intersecting[n]
                for o in counts[x, y]:
                    intersecting[n].add(o)
                    intersecting[o].add(n)
                counts[x, y].add(n)

p1 = sum(1 for v in counts.values() if len(v) > 1)
p2 = next(k for k,v in intersecting.items() if not v)

print('part1:', p1)
print('part2:', p2)

assert p1 == 113716
assert p2 == 742
