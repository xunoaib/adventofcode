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

maxrow = max(r for r,c in grid)
maxcol = max(c for r,c in grid)

walls = {p for p,ch in grid.items() if ch == '#'}
pos = next(p for p,ch in grid.items() if ch == '^')

visited = set()

a1 = a2 = 0

while pos in grid:
    visited.add(pos)

    r,c = pos
    np = r+DIRS[d][0], c + DIRS[d][1]
    if grid.get(np) == '#':
        d += 1
        d %= 4
    else:
        pos = np

    # for r in range(maxrow+1):
    #     for c in range(maxcol+1):
    #         print('X' if (r,c) in visited else grid[r,c], end='')
    #     print()
    # print()
    # time.sleep(0.1)

print('part1:', len(visited))
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
