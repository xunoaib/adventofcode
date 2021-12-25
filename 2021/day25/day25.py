#!/usr/bin/env python3
import copy
import sys
from itertools import count


def part1(grid):
    last_state = grid
    for step in count(1):
        grid = move_right(grid)
        grid = move_down(grid)
        if grid == last_state:
            return step
        last_state = grid


def move_right(grid):
    newgrid = copy.deepcopy(grid)
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            nc = (c - 1) % len(grid[0])
            leftchar = grid[r][nc]
            if ch == '.' and leftchar == '>':
                newgrid[r][c] = '>'
                newgrid[r][nc] = '.'
    return newgrid


def move_down(grid):
    newgrid = copy.deepcopy(grid)
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            nr = (r - 1) % len(grid)
            upchar = grid[nr][c]
            if ch == '.' and upchar == 'v':
                newgrid[r][c] = 'v'
                newgrid[nr][c] = '.'
    return newgrid


def main():
    grid = [list(line) for line in sys.stdin.read().strip().split('\n')]

    ans1 = part1(grid)
    print('part1:', ans1)
    assert ans1 == 412


if __name__ == '__main__':
    main()
