#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from functools import cache
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff and coff):
            yield r + roff, c + coff

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
    q = [(0, start)]
    visited = {start}

    while q:
        cost, p = heappop(q)
        if p == end:
            return cost

        for n in neighbors4(*p):
            if n in track and n not in visited:
                newcost = cost + 1
                visited.add(n)
                heappush(q, (newcost, n))

fastest_time = shortest_nocheat()

q = [(0, start, False)]
best = {(start, False): 0}
parent = {}

while q:
    cost, p, cheated = heappop(q)
    if p == end:
        print('yay', fastest_time - cost, (p, cheated))

        path = [p]
        while res := parent.get((p, cheated)):
            p, cheated = res
            path.append(p)
            # print((p,cheated))
        print_grid(path)
        break

    for n in neighbors4(*p):
        if n in track:
            newcost = cost + 1
            if best.get((n, cheated), sys.maxsize) > newcost:
                best[(n, cheated)] = newcost
                parent[(n, cheated)] = p, cheated
                heappush(q, (newcost, n, cheated))
        elif n in walls and not cheated:
            newcost = cost + 2
            for n in cheat_neighbors(*p):
                if n in track:
                    if best.get((n, True), sys.maxsize) > newcost:
                        parent[(n, True)] = p, cheated
                        best[(n, True)] = newcost
                        heappush(q, (newcost, n, True))
