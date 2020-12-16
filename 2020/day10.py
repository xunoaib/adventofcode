#!/usr/bin/env python
import sys
from collections import Counter

# map each adapter to possible outputs
adapters = {int(x): set() for x in sys.stdin}

# add start and end adapters
adapters[0] = set()
adapters[max(adapters)+3] = set()

# create graph of possible adapter outputs
for x in adapters:
    for i in range(x-3, x):
        if i in adapters:
            adapters[i].add(x)

# part 1 - traverse adapters, always selecting the lowest joltage
visited = [0]
while options := adapters[visited[-1]]:
    visited.append(min(options))

count = Counter(visited[i+1] - visited[i] for i in range(len(visited)-1))
print('part1:', count[1] * count[3])

# part 2 - count and cache the number of permutations for each adapter
totals = {}
def count_permutations(value):
    if value not in totals:
        totals[value] = sum(map(count_permutations, adapters[value])) or 1
    return totals[value]

print('part2:', count_permutations(0))
