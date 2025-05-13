#!/usr/bin/env python3
import sys
from collections import Counter

lines = sys.stdin.read().strip().split('\n')

count2 = count3 = 0

for line in lines:
    freq = Counter(line)
    count2 += 2 in freq.values()
    count3 += 3 in freq.values()

a1 = count2 * count3

print('part1:', a1)

assert a1 == 8820
