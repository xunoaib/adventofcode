#!/usr/bin/env python3

import sys
import time

lines = sys.stdin.read().strip().split('\n')

U,R,D,L = DIRS  = (-1,0), (0,1), (1,0),(0,-1)
d = 0

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

walls = {p for p,ch in grid.items() if ch == '#'}
start = next(p for p,ch in grid.items() if ch == '^')

a1 = a2 = 0

visited_p1 = set()

def part1():
    pos = start
    d = 0

    while pos in grid:
        visited_p1.add(pos)
        r,c = pos
        np = r+DIRS[d][0], c + DIRS[d][1]
        if grid.get(np) == '#':
            d += 1
            d %= 4
        else:
            pos = np
    return len(visited_p1)

def loops(block):
    g = grid.copy()
    g[block] = '#'
    pos = start
    d = 0
    states = set()
    visited = set()

    while pos in g:
        visited.add(pos)
        if (pos, d) in states:
            return True
        states.add((pos, d))

        r,c = pos
        np = r + DIRS[d][0], c + DIRS[d][1]
        if g.get(np) == '#':
            d += 1
            d %= 4
        else:
            pos = np

        # maxrow = max(r for r,c in grid)
        # maxcol = max(c for r,c in grid)
        # for r in range(maxrow+1):
        #     for c in range(maxcol+1):
        #         print('X' if (r,c) in visited else grid[r,c], end='')
        #     print()
        # print()
        # time.sleep(0.1)

    return False

a1 = part1()
a2 = sum([loops(p) for p in visited_p1 if p != start])

print('part1:', a1)
print('part2:', a2)

assert a1 == 5453
assert a2 == 2188
