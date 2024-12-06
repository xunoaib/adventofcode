#!/usr/bin/env python3

import sys

DIRS = (-1,0), (0,1), (1,0), (0,-1)

lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

start = next(p for p,ch in grid.items() if ch == '^')

def run(grid):
    p = start
    d = 0

    visited = set()
    states = set()

    while p in grid:
        visited.add(p)
        if (p, d) in states:
            return visited, True
        states.add((p, d))

        np = p[0] + DIRS[d][0], p[1] + DIRS[d][1]
        if grid.get(np) == '#':
            d = (d + 1) % 4
        else:
            p = np

    return visited, False

visited_p1, _ = run(grid)

a1 = len(visited_p1)
a2 = sum(run(grid | {p: '#'})[1] for p in visited_p1 if p != start)

print('part1:', a1)
print('part2:', a2)

assert a1 == 5453
assert a2 == 2188
