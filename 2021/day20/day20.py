#!/usr/bin/env python3
from itertools import product
import sys


def grid_neighbors(offsets):
    def gen(grid, r, c):
        for roff, coff in offsets:
            yield r + roff, c + coff
    return gen


neighbors8 = grid_neighbors([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0),
                             (0, 1), (1, -1), (1, 0), (1, 1)])

bg = '.'


def getch(grid, nr, nc):
    ch, b = '#.' if bg == '.' else '.#'
    return ch if (nr, nc) in grid else b


def get_index(grid, r, c):
    s = ''.join(getch(grid, nr, nc) for nr, nc in neighbors8(grid, r, c))
    return int(s.replace('.', '0').replace('#', '1'), 2)


def step(lookup, grid):
    """Apply image enhancement, only tracking pixels different from the background.
    The empty and infinite background might invert itself every tick based on the first and last lookup entries (0, len-1).
    This behavior does NOT occur in the web example, as lookup[0] = '.' and lookup[-1] = '#'
    """
    global bg
    newg = {}
    minr, minc, maxr, maxc = get_bounds(grid)
    for r, c in product(range(minr - 1, maxr + 2), range(minc - 1, maxc + 2)):
        idx = get_index(grid, r, c)
        ch = lookup[idx]
        if ch == bg:
            newg[(r, c)] = ch

    bg = '#' if bg == '.' else '.'
    return newg


def print_grid(grid):
    minr, minc, maxr, maxc = get_bounds(grid)
    for r in range(minr, maxr + 1):
        for c in range(minc, maxc + 1):
            print(getch(grid, r, c), end='')
        print('')


def get_bounds(grid):
    rows, cols = zip(*grid)
    return min(rows), min(cols), max(rows), max(cols)


def part1(lookup, grid):
    global bg
    for i in range(2):
        grid = step(lookup, grid)
    return len(grid)


def part2(lookup, grid):
    global bg
    bg = '.'
    for i in range(50):
        # print(f'{i+1} ', end='', flush=True)
        grid = step(lookup, grid)
    return len(grid)


def main():
    lookup, grid = sys.stdin.read().strip().split('\n\n')
    grid = grid.split('\n')

    g = {(r, c): grid[r][c]
         for r, c in product(range(len(grid)), range(len(grid[0])))
         if grid[r][c] != bg}

    ans1 = part1(lookup, g)
    print('part1:', ans1)

    ans2 = part2(lookup, g)
    print('part2:', ans2)

    assert ans1 == 5571
    assert ans2 == 17965


if __name__ == '__main__':
    main()
