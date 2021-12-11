#!/usr/bin/env python3
import copy
import sys
from itertools import product

def get_adjacent(grid, point):
    r, c = point
    for roff, coff in product([-1,0,1], [-1,0,1]):
        if roff == coff == 0:
            continue
        nr, nc = r + roff, c + coff
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
            yield nr, nc

def find_new_flashes(grid, flashpoints):
    flashed = False
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if (r,c) in flashpoints:
            continue
        if grid[r][c] > 9:
            flashpoints.add((r,c))
            flashed = True
            for nr, nc in get_adjacent(grid, (r,c)):
                grid[nr][nc] += 1
    return flashed

def step(grid):
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        grid[r][c] += 1

    flashpoints = set()
    while find_new_flashes(grid, flashpoints):
        pass

    for r,c in flashpoints:
        grid[r][c] = 0

    return len(flashpoints)

def part1(grid):
    grid = copy.deepcopy(grid)
    return sum(step(grid) for _ in range(100))

def part2(grid):
    grid = copy.deepcopy(grid)
    i = 0
    while True:
        i += 1
        if step(grid) == len(grid) * len(grid[0]):
            return i

def main():
    grid = sys.stdin.read().strip().split()
    grid = [list(map(int, row)) for row in grid]

    ans1 = part1(grid)
    print('part1:', ans1)

    ans2 = part2(grid)
    print('part2:', ans2)

    assert ans1 == 1659
    assert ans2 == 227

if __name__ == '__main__':
    main()
