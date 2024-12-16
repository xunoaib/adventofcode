#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)
DIRS = U, R, D, L


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield (r + roff, c + coff), DIRS.index((roff, coff))

def print_grid(grid):
    maxr = max(r for r,c in grid)
    maxc = max(c for r,c in grid)

    for r in range(maxr+1):
        for c in range(maxc+1):
            print(grid[r,c], end='')
        print()
    print()

lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

walls = {p for p, ch in grid.items() if ch == '#'}
pos = start = next(p for p, ch in grid.items() if ch == 'S')
end = next(p for p, ch in grid.items() if ch == 'E')
d = DIRS.index(R)

def turn_cost(d, e):
    dist = abs(d - e)
    if dist > 2:
        dist -= 2
    return 1000 * dist

# print(turn_cost(0,1))
# print(turn_cost(1,2))
# print(turn_cost(1,1))
# print(turn_cost(1,3))
# print(turn_cost(4,1))
# exit(0)

q = [(0, pos, d)]
seen = {pos: 0}

parents = {}

# for n, nd in neighbors4(*pos):
#     if n in walls:
#         continue
#     print(n, nd, turn_cost(d,nd))
# exit(0)

while q:
    cost, pos, d = heappop(q)
    print('>>> AT', pos, d, cost)
    if pos == end:
        print('part1:', cost)
        break
    for n, nd in neighbors4(*pos):
        newcost = cost + 1 + turn_cost(d, nd)
        if n not in walls and seen.get(n, sys.maxsize) > newcost:
            parents[n] = pos
            print('>>> NX', n, nd, newcost)
            heappush(q, (newcost, n, nd))
            seen[n] = newcost

g = grid.copy()
n = end
while n := parents.get(n):
    g[n] = '\033[91mX\033[0m'
print_grid(g)
