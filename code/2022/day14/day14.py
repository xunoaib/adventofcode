#!/usr/bin/env python3
import re
import sys
from itertools import pairwise

SAND_SOURCE = (500, 0)


def drop_sand(grid, abyss, pos=SAND_SOURCE):
    x, y = pos

    if y >= abyss:
        grid[pos] = 'o'
        return True

    for pos2 in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
        if not grid.get(pos2):
            return drop_sand(grid, abyss, pos2)

    grid[pos] = 'o'


def main():
    lines = sys.stdin.read().strip().split('\n')

    grid = {}
    for line in lines:
        points = [
            tuple(map(int, xy.split(',')))
            for xy in re.findall(r'\d+,\d+', line)
        ]

        for p1, p2 in pairwise(points):
            xoff = p2[0] - p1[0]
            yoff = p2[1] - p1[1]

            if xoff:
                xoff //= abs(xoff)
            else:
                yoff //= abs(yoff)

            x, y = p1
            while (x, y) != p2:
                grid[(x, y)] = '#'
                x += xoff
                y += yoff
            grid[p2] = '#'

    abyss = max(y for x, y in grid.keys())

    grid_orig = grid.copy()
    ans1 = 0
    while not drop_sand(grid, abyss):
        ans1 += 1
    print('part1:', ans1)

    grid = grid_orig.copy()
    ans2 = 0
    while not grid.get(SAND_SOURCE):
        drop_sand(grid, abyss + 1)
        ans2 += 1
    print('part2:', ans2)

    assert ans1 == 692
    assert ans2 == 31706


if __name__ == '__main__':
    main()
