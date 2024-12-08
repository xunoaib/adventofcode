#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import combinations

lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

fpositions = defaultdict(set)
for pos, f in grid.items():
    if f != '.':
        fpositions[f].add(pos)

antinodes1 = set()
antinodes2 = set()

for f, positions in fpositions.items():
    for p1,p2 in combinations(positions, r=2):

        rdiff = p2[0] - p1[0]
        cdiff = p2[1] - p1[1]

        antinodes1 |= {
            (p1[0] - rdiff, p1[1] - cdiff),
            (p2[0] + rdiff, p2[1] + cdiff)
        }

        p = p1
        while p in grid:
            antinodes2.add(p)
            p = p[0] - rdiff, p[1] - cdiff

        p = p1
        while p in grid:
            antinodes2.add(p)
            p = p[0] + rdiff, p[1] + cdiff

a1 = len(antinodes1 & set(grid))
a2 = len(antinodes2 & set(grid))

print('part1:', a1)
print('part2:', a2)

assert a1 == 357
assert a2 == 1266
