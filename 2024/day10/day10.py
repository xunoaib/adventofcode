#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

import numpy as np

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff and coff):
            yield r + roff, c + coff

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


lines = sys.stdin.read().strip().split('\n')

g = {
    (r, c): int(ch)
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
    if ch != '.'
}

def find_paths(r,c):
    orig_r, orig_c = r,c
    q = [(r,c)]
    trails = set()
    while q:
        r,c = q.pop()
        print((r,c), g[r,c], q)
        if g[r,c] == 9:
            trails.add((orig_r, orig_c, r,c))

        for nr, nc in neighbors4(r,c):
            if (nr,nc) in g and g[nr,nc] == g[r,c] + 1:
                q.append((nr,nc))
    return trails

trails = set()
for (r,c), v in g.items():
    if v == 0:
        print('runing tail', (r,c),v)
        trails |= find_paths(r,c)

a1 = len(trails)

print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
