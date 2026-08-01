#!/usr/bin/env python3
import operator
import sys
from itertools import permutations
from functools import reduce

def get_adjacent(grid, point):
    r, c = point
    for roff, coff in permutations([-1, 0, 1], 2):
        if 0 not in (roff, coff):
            continue
        nr, nc = r + roff, c + coff
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc

def get_basin_points(grid, point):
    visited, basin = set(), set()
    frontier = [point]

    while frontier:
        point = r, c = frontier.pop(0)
        if grid[r][c] == 9:
            continue

        basin.add(point)
        for newpt in get_adjacent(grid, point):
            if newpt not in visited:
                visited.add(newpt)
                frontier.append(newpt)
    return basin

def find_low_points(grid):
    points = set()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            for nr, nc in get_adjacent(grid, (r, c)):
                if grid[nr][nc] <= val:
                    break
            else:
                points.add((r, c))
    return points

def part1(grid):
    points = find_low_points(grid)
    return sum(grid[r][c] + 1 for r, c in points)

def part2(grid):
    points = find_low_points(grid)
    basin_sizes = sorted(len(get_basin_points(grid, point)) for point in points)
    return reduce(operator.mul, basin_sizes[-3:])

def main():
    grid = sys.stdin.read().strip().split()
    grid = [list(map(int, row)) for row in grid]

    ans1 = part1(grid)
    print('part1:', ans1)

    ans2 = part2(grid)
    print('part2:', ans2)

    assert ans1 == 570
    assert ans2 == 899392

if __name__ == '__main__':
    main()
