#!/usr/bin/env python3
import sys
from functools import cache

DIRS = L, R, U, D = (0, -1), (0, 1), (-1, 0), (1, 0)


class Solver:

    def __init__(self, grid):
        self.grid = grid

    def neighbors(self, r, c):
        for roff, coff in DIRS:
            npos = r + roff, c + coff
            if self.grid.get(npos, '#') in 'S.':
                yield npos

    @cache
    def find_plots(self, pos, stepsleft):
        if stepsleft == 0:
            return {pos}
        result = set()
        for neighbor in self.neighbors(*pos):
            result |= self.find_plots(neighbor, stepsleft - 1)
        return result


def draw_plots(grid, plots):
    maxr, maxc = map(max, zip(*grid))
    for r in range(maxr + 1):
        for c in range(maxc + 1):
            ch = 'O' if (r, c) in plots else grid[r, c]
            print(ch, end='')
        print()


def main():
    lines = sys.stdin.read().strip().split('\n')

    g = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
    }

    s = Solver(g)
    start = [pos for pos, ch in g.items() if ch == 'S'][0]
    plots = s.find_plots(start, 64)
    a1 = len(plots)
    print('part1:', a1)
    assert a1 == 3770


if __name__ == '__main__':
    main()
