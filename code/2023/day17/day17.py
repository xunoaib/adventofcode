#!/usr/bin/env python3
import sys
from collections import Counter
from heapq import heappop, heappush

DIRS = U, D, L, R = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbors1(grid, gscores, current):
    r, c, lastdir, dircount = current
    for roff, coff in DIRS:
        nr = r + roff
        nc = c + coff
        if (nr, nc) not in grid:
            continue
        if lastdir == (-roff, -coff):
            continue

        ngscore = gscores[current] + grid[nr, nc]
        if (roff, coff) != lastdir:
            ndircount = 1  # changed direction
        elif dircount < 3:
            ndircount = dircount + 1
        else:
            continue  # exceeded 3 blocks in one direction

        yield ngscore, (nr, nc, (roff, coff), ndircount)


def neighbors2(grid, gscores, current):
    r, c, lastdir, dircount = current
    for roff, coff in DIRS:
        nr = r + roff
        nc = c + coff
        if (nr, nc) not in grid:
            continue
        if lastdir == (-roff, -coff):
            continue

        ngscore = gscores[current] + grid[nr, nc]
        if (roff, coff) != lastdir:
            ndircount = 4  # always walk 4 blocks in a new direction
            for _ in range(3):
                nr += roff
                nc += coff
                ngscore += grid.get((nr, nc), 0)
            if (nr, nc) not in grid:
                continue
        elif dircount < 10:
            ndircount = dircount + 1
        else:
            continue  # >10 consecutive blocks (invalid)

        yield ngscore, (nr, nc, (roff, coff), ndircount)


def solve(grid, neighbors):

    def h(row, col):
        return abs(maxr - row) + abs(maxc - col)

    maxr = max(r for r, _ in grid)
    maxc = max(c for _, c in grid)

    r = c = 0
    current = (r, c, None, 0)
    gscores = {current: 0}
    fscores = {current: h(r, c)}
    cameFrom = {current: None}
    counter = Counter({current: 1})
    q = [(fscores[current], current)]

    while q:
        _, current = heappop(q)
        r, c = current[0:2]
        current = tuple(current)
        counter[current] -= 1

        if (r, c) == (maxr, maxc):
            return gscores[current]

        for ngscore, neighbor in neighbors(grid, gscores, current):
            if ngscore < gscores.get(neighbor, sys.maxsize):
                cameFrom[neighbor] = current
                gscores[neighbor] = ngscore
                fscores[neighbor] = ngscore + h(*neighbor[0:2])
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

    a1 = solve(grid, neighbors1)
    print('part1:', a1)

    a2 = solve(grid, neighbors2)
    print('part2:', a2)

    assert a1 == 907
    assert a2 == 1057


if __name__ == '__main__':
    main()
