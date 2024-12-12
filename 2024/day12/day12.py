#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import pairwise


def neighbors4(r, c):
    for roff, coff in (-1, 0), (1, 0), (0, -1), (0, 1):
        if not (roff and coff):
            yield r + roff, c + coff

def find_pool(pos):
    ch = grid[pos]
    pool = {pos}
    q = [pos]
    while q:
        pos = q.pop()
        for n in neighbors4(*pos):
            if n not in pool and grid.get(n) == ch:
                pool.add(n)
                q.append(n)
    return pool

def find_pools():
    pools = []
    pooled = set()
    for p in grid:
        if p not in pooled:
            pool = find_pool(p)
            pools.append(pool)
            pooled |= pool
    return pools

def find_border_vectors(pool):
    borders = set()
    for p in pool:
        for n in neighbors4(*p):
            if n not in pool:
                borders.add((p, sub(n,p)))
    return borders

def sub(a,b):
    return b[0]-a[0], b[1]-a[1]

grid = {
    (r, c): ch
    for r, line in enumerate(sys.stdin)
    for c, ch in enumerate(line.strip())
}

pools = find_pools()

a1 = sum(len(pool) * sum(n not in pool for p in pool for n in neighbors4(*p)) for pool in pools)
a2 = 0

for pool in pools:
    borders = find_border_vectors(pool)

    vec_tiles = defaultdict(set)
    for p, vec in borders:
        vec_tiles[vec].add(p)

    sides = 0
    for vec, tiles in vec_tiles.items():
        coff, roff = vec  # flip axes to get fence direction
        tiles = sorted(tiles, key=lambda v: v if coff else v[::-1])
        sides += 1 + sum(tuple(map(abs, sub(b, a))) != (abs(roff), abs(coff)) for a,b in pairwise(tiles))

    a2 += len(pool) * sides

print('part1:', a1)
print('part2:', a2)

assert a1 == 1424006
assert a2 == 858684
