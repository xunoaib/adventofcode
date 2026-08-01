#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

from scipy.interpolate import lagrange

DIRS = L, R, U, D = (0, -1), (0, 1), (-1, 0), (1, 0)


class Solver:

    def __init__(self, grid):
        self.grid = grid
        self.rows = max(r for r, _ in grid) + 1
        self.cols = max(c for _, c in grid) + 1

    def neighbors_part1(self, r, c):
        for roff, coff in DIRS:
            npos = r + roff, c + coff
            if self.grid.get(npos, '#') in 'S.':
                yield npos

    def neighbors_part2(self, r, c):
        for roff, coff in DIRS:
            npos = nr, nc = r + roff, c + coff
            if self.grid.get((nr % self.rows, nc % self.cols), '#') in 'S.':
                yield npos

    def find_accessible(self, nsteps, neighbor_func):
        '''Find every reachable position from the current location using a given number of steps'''

        start = [pos for pos, ch in self.grid.items() if ch == 'S'][0]
        q = [(0, start)]
        seen = {start}
        landed = set()
        while q:
            cost, pos = heappop(q)
            if cost % 2 == nsteps % 2:
                landed.add(pos)
            if cost >= nsteps:
                continue
            for neighbor in neighbor_func(*pos):
                if neighbor not in seen:
                    seen.add(neighbor)
                    heappush(q, (cost + 1, neighbor))
        return landed

    def part1(self, nsteps=64):
        visited = self.find_accessible(nsteps, self.neighbors_part1)
        return len(visited)

    def part2(self, nsteps=26501365):
        assert (nsteps - 65) % 131 == 0
        counts = [
            len(self.find_accessible(65 + i * 131, self.neighbors_part2))
            for i in range(3)
        ]
        poly = lagrange(*zip(*enumerate(counts)))
        return int(poly((nsteps - 65) // 131))


def main():
    lines = sys.stdin.read().strip().split('\n')
    grid = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
    }

    s = Solver(grid)

    a1 = s.part1()
    print('part1:', a1)

    a2 = s.part2()
    print('part2:', a2)

    assert a1 == 3770
    assert a2 == 628206330073385


if __name__ == '__main__':
    main()
