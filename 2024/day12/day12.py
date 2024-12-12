#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import pairwise

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

a1 = 0
for pool in pools:
    perim = find_perim(pool)
    area = len(pool)
    a1 += perim * area
print('part1:', a1)

def sub(a,b):
    return b[0]-a[0], b[1]-a[1]

def find_borders(pool):
    borders = set()
    for p in pool:
        for n in neighbors4(*p):
            if n not in pool:
                borders.add((p, sub(n,p)))
    return borders

a2 = 0
for pool in pools:
    borders = find_borders(pool)

    sided = defaultdict(set)
    for p, diff in borders:
        sided[diff].add(p)

    ch = grid[list(pool)[0]]

    # if ch not in 'V':
    #     continue

    sides = 0
    for diff, poss in sided.items():
        coff, roff = diff
        poss = sorted(poss) if coff else sorted(poss, key=lambda v: v[::-1])

        # print(diff, '=>', poss)

        sides += 1  # at least one side
        for a,b in pairwise(poss):
            if tuple(map(abs, sub(b, a))) == (abs(roff), abs(coff)):
                # print('    adjacent    ', a, b, diff)
                sides += 0  # same side
            else:
                sides += 1  # new side
                # print('    not adjacent', a, b, diff)

    # print(ch, len(pool), '*', sides, '=', len(pool)  * sides)
    a2 += len(pool)  * sides


print('part2:', a2)

assert a1 == 1424006
assert a2 == 858684
