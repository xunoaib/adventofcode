#!/usr/bin/env python3
# import copy
# import re
# import numpy as np
from collections import Counter
from functools import cache
from itertools import product
from heapq import heappop, heappush
import sys

DIRS = U, D, L, R = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors(grid, current):
    r, c, lastdir, dircount = current
    # for roff, coff in product([-1, 0, 1], repeat=2):
    for roff, coff in DIRS:
        if roff == coff == 0 or 0 not in (roff, coff):
            continue
        if lastdir == (-roff, -coff):
            continue
        nr = r + roff
        nc = c + coff
        if (nr, nc) not in grid:
            continue
        newdircount = (dircount + 1) if lastdir == (roff, coff) else 1
        if newdircount <= 3:
            yield nr, nc, (roff, coff), newdircount


def part1(grid):

    def h(row, col):
        return abs(maxr - row) + abs(maxc - col)

    def reconstruct_path(node):
        path = []
        while node:
            path.append(node)
            node = cameFrom[node]
        return path

    def print_path(path):
        g = grid.copy()
        while path:
            r, c, d, _ = path.pop()
            g[r,c] = f'\033[91;1m{g[r,c]}\033[0m'

        for r in range(maxr+1):
            for c in range(maxc+1):
                print(g[r,c], end='')
            print()
        print()

    maxr = max(r for r, _ in grid)
    maxc = max(c for _, c in grid)
    goal = (maxr, maxc)

    gscores = {}
    fscores = {}
    cameFrom = {}
    counter = Counter()

    pos = (0, 0)
    current = (*pos, None, 0)
    gscores[current] = 0
    fscores[current] = gscores[current] + h(*pos)
    counter[current] += 1
    cameFrom[current] = None

    q = [(fscores[current], (*pos, None, 0))]

    while q:
        _, current = _, (r, c, _, _) = heappop(q)
        current = tuple(current)
        counter[current] -= 1

        if (r, c) == goal:
            path = reconstruct_path(current)
            print_path(path)
            return gscores[current]

        for neighbor in neighbors(grid, current):
            npos = neighbor[0:2]
            ngscore = gscores[current] + grid[npos]
            if ngscore < gscores.get(neighbor, sys.maxsize):
                cameFrom[neighbor] = current
                gscores[neighbor] = ngscore
                fscores[neighbor] = ngscore + h(*npos)
                if counter[neighbor] == 0:
                    counter[neighbor] += 1
                    heappush(q, (fscores[neighbor], neighbor))


def main():
    lines = sys.stdin.read().strip().split('\n')

    grid = {
        (r, c): int(ch)
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
    }

    a1 = part1(grid)
    print('part1:', a1)

if __name__ == '__main__':
    main()
