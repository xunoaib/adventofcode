#!/usr/bin/env python3
import sys
from heapq import heappop, heappush


def neighbors(grid, r, c):
    for roff, coff in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        nr, nc = r + roff, c + coff
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


def neighbors2(grid, r, c):
    for roff, coff in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        nr, nc = r + roff, c + coff
        if 0 <= nr < len(grid) * 5 and 0 <= nc < len(grid[0]) * 5:
            yield nr, nc


def dijkstra(grid, start, end):
    frontier = [(0, start)]
    visited = set()

    while frontier:
        cost, pos = heappop(frontier)
        if pos == end:
            return cost

        if pos in visited:
            continue
        visited.add(pos)

        for nr, nc in neighbors(grid, *pos):
            if (nr, nc) not in visited:
                heappush(frontier, (cost + grid[nr][nc], (nr, nc)))


def dijkstra2(grid, start, end):
    frontier = [(0, start)]
    visited = set()
    rows, cols = len(grid), len(grid[0])

    while frontier:
        cost, pos = heappop(frontier)
        if pos == end:
            return cost

        if pos in visited:
            continue
        visited.add(pos)

        for nr, nc in neighbors2(grid, *pos):
            if (nr, nc) not in visited:
                newrisk = grid[nr % rows][nc % cols] + nr // rows + nc // cols
                newrisk = (newrisk - 1) % 9 + 1
                heappush(frontier, (cost + newrisk, (nr, nc)))


def main():
    grid = sys.stdin.read().strip().split('\n')
    grid = [list(map(int, line)) for line in grid]

    rows, cols = len(grid), len(grid[0])

    ans1 = dijkstra(grid, (0, 0), (rows - 1, cols - 1))
    print('part1:', ans1)

    ans2 = dijkstra2(grid, (0, 0), (rows * 5 - 1, cols * 5 - 1))
    print('part2:', ans2)

    assert ans1 == 540
    assert ans2 == 2879


if __name__ == '__main__':
    main()
