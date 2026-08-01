#!/usr/bin/env python3

import sys
from collections import Counter

x = []
y = []

for line in sys.stdin:
    a,b = map(int, line.split())
    x.append(a)
    y.append(b)

x.sort()
y.sort()

c = Counter(y)

ans1 = sum(abs(a-b) for a,b in zip(x,y))
ans2 = sum(c[a] * a for a in x)

print('part1:', ans1)
print('part2:', ans2)
