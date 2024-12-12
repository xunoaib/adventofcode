#!/usr/bin/env python3

import sys
from collections import defaultdict

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff

lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

def find_perim(locs):
    tot = 0
    for p in locs:
        for n in neighbors4(*p):
            if n not in locs:
                tot += 1
    return tot

def find_pool(r,c):
    ch = grid[r,c]
    pool = {(r,c)}
    seen = {(r,c)}
    q = [(r,c)]
    while q:
        p = q.pop()
        for n in neighbors4(*p):
            if n not in seen and grid.get(n) == ch:
                seen.add(n)
                q.append(n)
                pool.add(n)
    return pool

pools = []
pooled = set()

for p, ch in grid.items():
    if p not in pooled:
        pool = find_pool(*p)
        pools.append(pool)
        pooled |= pool
        # print('new pool', ch, 'at', p, pool)
        # print('new pool', ch)

# groups = defaultdict(set)
# for (r,c), ch in grid.items():
#     groups[ch].add((r,c))

a1 = 0
for pool in pools:
    perim = find_perim(pool)
    area = len(pool)
    # print(ch, p, a, perim*are)
    a1 += perim * area

print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
