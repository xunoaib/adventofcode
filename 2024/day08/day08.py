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

freqposs = defaultdict(set)
for p, f in grid.items():
    if f != '.':
        freqposs[f].add(p)
freqposs  = dict(freqposs)

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

        q = r1, c1
        while q in grid:
            # if q not in (p1, p2):
            antinodes.add(q)
            q = q[0] - rdiff, q[1] - cdiff

        q = r1, c1
        while q in grid:
            # if q not in (p1, p2):
            antinodes.add(q)
            q = q[0] + rdiff, q[1] + cdiff

        # p4 = r2 + rdiff, c2 + cdiff
        # assert not {q, p4} & {p1, p2}

        # antinodes |= {q,p4}

antinodes = {(r,c) for (r,c) in antinodes if r in range(maxrow+1) and c in range(maxcol+1)}

for r,c in antinodes:
    g[r,c] = '#'

for r in range(maxrow+1):
    for c in range(maxcol+1):
        print(g[r,c], end='')
    print()

a2 = len(antinodes)

print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
