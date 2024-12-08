#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from itertools import combinations, pairwise, permutations, product

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)


lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

maxrow = max(r for r,c in grid.keys())
maxcol = max(c for r,c in grid.keys())

# grid  = {k: v for k,v in grid.items() if v != '.'}

freqposs = defaultdict(set)
for p, f in grid.items():
    if f != '.':
        freqposs[f].add(p)
freqposs  = dict(freqposs)

# __import__('pprint').pprint(freqposs)
# exit(0)

antinodes = set()

g = grid.copy()

for f, positions in freqposs.items():
    print('positinos:', positions)
    for p1,p2 in combinations(positions, r=2):
        print(p1, p2)

        r1,c1 = p1
        r2,c2 = p2
        rdiff = r2-r1
        cdiff = c2-c1

        p3 = r1 - rdiff, c1 - cdiff
        p4 = r2 + rdiff, c2 + cdiff
        assert not {p3, p4} & {p1, p2}

        antinodes |= {p3,p4}

antinodes = {(r,c) for (r,c) in antinodes if r in range(maxrow+1) and c in range(maxcol+1)}

for r,c in antinodes:
    g[r,c] = '#'

for r in range(maxrow+1):
    for c in range(maxcol+1):
        print(g[r,c], end='')
    print()

a1 = a2 = 0
a1 = len(antinodes)

print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
