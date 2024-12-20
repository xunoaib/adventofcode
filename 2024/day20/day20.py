#!/usr/bin/env python3

import sys
from collections import Counter
from functools import cache
from heapq import heappop, heappush

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


@cache
def cheat_neighbors(r, c):
    neighbors = set()
    for n in neighbors4(r, c):
        neighbors.add(n)
        for p in neighbors4(*n):
            neighbors.add(p)
    return neighbors

def sub(a,b):
    return b[0]-a[0], b[1]-a[1]

def add(a,b):
    return b[0]+a[0], b[1]+a[1]

def print_grid(path):
    rows = 1 + max(r for r,c in grid)
    cols = 1 + max(c for r,c in grid)
    for r in range(rows):
        for c in range(rows):
            ch = '\033[91mX\033[0m' if (r,c) in path else grid[r,c]
            print(ch, end='')
        print()

lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

walls = {p for p, ch in grid.items() if ch == '#'}
start = next(p for p, ch in grid.items() if ch == 'S')
end = next(p for p, ch in grid.items() if ch == 'E')
track = {p for p, ch in grid.items() if ch != '#'}

grid[start] = '.'
grid[end] = '.'

a1 = a2 = 0

def shortest_nocheat():
    q = [(0, end)]
    children = {}
    costs = {end: 0}

    while q:
        cost, p = heappop(q)
        for n in neighbors4(*p):
            if n in track and n not in costs:
                children[n] = p
                costs[n] = cost + 1
                heappush(q, (cost + 1, n))

    assert len(costs) == len(track)
    return costs, children

fastest_times, all_children = shortest_nocheat()
fastest_time = fastest_times[start]

path = [start]
p = start
while p := all_children.get(p):
    path.append(p)

savings = {}
for cost, src in enumerate(path):
    for tar in cheat_neighbors(*src):
        if tar in track and tar != src:
            savings[src,tar] = fastest_times[src] - fastest_times[tar] - 2

counts = Counter(savings.values())

a1 = 0
for t, freq in sorted(counts.items(), reverse=True):
    if t >= 100:
        a1 += freq

print('part1:', a1)
