#!/usr/bin/env python3

import sys

groups = sys.stdin.read().strip().split('\n\n')

keys = []
locks = []

for group in groups:

    lines  = group.strip().split('\n')

    grid = {
        (r, c)
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
        if ch == '#'
    }

    if all((0,c) in grid for c in range(5)):
        locks.append(grid)
    else:
        keys.append(grid)

a1 = 0
for key in keys:
    for lock in locks:
        if not key & lock:
            a1 += 1

print('part1:', a1)
assert a1 == 3619
