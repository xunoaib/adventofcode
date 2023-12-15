#!/usr/bin/env python3
import sys
from time import time


def settle_step(grid):
    g = {}
    for (r, c), ch in grid.items():
        if r > 0 and ch == 'O' and grid.get((r - 1, c), '.') == '.':
            g[r, c] = '.'
            g[r - 1, c] = 'O'
    return grid | g


def settle(grid):
    while (newgrid := settle_step(grid)) != grid:
        grid = newgrid
    return grid


def rotate(grid):
    max_r = max(r for r, _ in grid)
    return {(c, max_r - r): ch for (r, c), ch in grid.items()}


def score(grid):
    load = 0
    max_r = max(r for r, _ in grid)
    for (r, _), ch in grid.items():
        if ch == 'O':
            load += max_r + 1 - r
    return load


def part2(grid):
    n = 1000000000 * 4  # 10e8 cycles x 4 rotations each
    seen, grids = {}, {}

    # perform transformations until a repeat is found
    last = time()
    for i in range(n):
        if time() - last > 2:
            print('iteration', i)
            last = time()
        grid = rotate(settle(grid))
        state = tuple(sorted(grid.items())) + (i % 4, )
        if start := seen.get(state):
            break
        seen[state] = i
        grids[i] = grid

    idx = start + (n - start - 1) % (i - start)
    return score(grids[idx])


def main():
    lines = sys.stdin.read().strip().split('\n')

    grid = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line) if ch != '.'
    }

    a1 = score(settle(grid))
    print('part1:', a1)

    a2 = part2(grid)
    print('part2:', a2)

    assert a1 == 110128
    assert a2 == 103861


if __name__ == '__main__':
    main()
