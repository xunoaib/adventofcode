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
        for n in neighbors4(*q.pop()):
            if n not in pool and grid.get(n) == ch:
                pool.add(n)
                q.append(n)
    return pool

def find_pools():
    pools = []
    unused = set(grid)
    while unused:
        pool = find_pool(unused.pop())
        pools.append(pool)
        unused -= pool
    return pools

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
    fence_vecs = {(p, sub(n,p)) for p in pool for n in neighbors4(*p) if n not in pool}
    vec_tiles = defaultdict(set)

    for p, vec in fence_vecs:
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
