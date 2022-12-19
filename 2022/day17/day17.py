#!/usr/bin/env python3
import itertools
import sys

rocks = [
    ['####'],
    '.#.\n###\n.#.'.split(),
    '..#\n..#\n###'.split(),
    ['#']*4,
    ['##', '##'],
]

MAX_X = 6

def can_fall(grid, x, y, rock):
    return valid_pos(grid, x, y - 1, rock)

def rock_to_coords(x, y, rock):
    for r, row in enumerate(rock):
        for c, ch in enumerate(row):
            if ch == '#':
                yield x + c, y + (len(rock) - 1 - r)

def valid_pos(grid, newx, newy, rock):
    for rx, ry in rock_to_coords(newx, newy, rock):
        if ry < 0 or rx < 0 or rx > MAX_X or (rx, ry) in grid:
            return False
    return True

def print_grid(grid):
    print('')
    if not grid:
        print('nothing')
        return

    max_height = max(y for x,y in grid)
    min_height = min(y for x,y in grid)
    print(f'y: {min_height} to {max_height}')

    for y in range(max_height, -1, -1):
        for x in range(8):
            ch = grid.get((x, y), '.')
            print(ch, end='')
        print()

def main():
    data = sys.stdin.read().strip()

    grid = {}
    max_height = 0

    rock_idx = 0
    x = 2
    y = max_height + 3
    fallen_count = 0

    for ch_idx in itertools.count():
        ch = data[ch_idx % len(data)]
        rock = rocks[rock_idx]
        xoff = 1 if ch == '>' else -1
        newx = max(0, min(6, x + xoff))
        newy = y - 1

        if valid_pos(grid, newx, y, rock):
            x = newx

        if valid_pos(grid, x, newy, rock):
            y = newy

        else:
            coords = list(rock_to_coords(x, y, rock))
            for coord in coords:
                grid[coord] = '#'

            x = 2
            y = 4 + max(y for x,y in grid)
            rock_idx += 1
            rock_idx %= len(rocks)

            fallen_count += 1
            if fallen_count >= 2022:
                print('part1:', y - 3)
                break

if __name__ == '__main__':
    main()
