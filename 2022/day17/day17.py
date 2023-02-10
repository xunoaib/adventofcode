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

def find_largest_repeat(grid):
    from collections import Counter

    ymax = max(y for x,y in grid)
    rows = [
        tuple(x for x in range(MAX_X + 1) if (x,y) in grid)
        for y in range(ymax + 1)
    ]

    # counts = Counter(rows)
    # __import__('pprint').pprint(counts.most_common())

    best = tuple()
    for ystart in range(3100, ymax):
        for length in range(1, (ymax + 1 - ystart) // 2):
            g1 = rows[ystart:ystart+length]
            g2 = rows[ystart+length:ystart+length*2]
            # TODO: also account for looping rock_idx and ch_idx!
            # if len(g1) != len(g2):
            #     print('error:', len(g1), len(g2))
            #     exit()
            if all(a == b for a,b in zip(g1, g2)):
                if len(g1) > len(best):
                    best = tuple(g1)
                    print(f'new best: {ystart=}, {length=}')

    # for y_start in range(ymax):
    #     for y in range(y_start, ymax):
    #         print(row)
    #     break

def main():
    data = sys.stdin.read().strip()

    grid = {}
    max_height = 0

    rock_idx = 0
    x = 2
    y = max_height + 3
    fallen_count = 0

    turn = 0  # keeps code warnings away
    for turn in itertools.count():
        turn, rock_idx, x, y, fallen_count = tick(grid, data, turn, rock_idx, x, y, fallen_count)
        if fallen_count >= 2022:
            print('part1:', y - 3)
            assert y - 3 == 3181
            break

    for _ in range(10000):
        turn, rock_idx, x, y, fallen_count = tick(grid, data, turn, rock_idx, x, y, fallen_count)

    print('finding largest repeat')
    find_largest_repeat(grid)

def tick(grid, data, turn, rock_idx, x, y, fallen_count):
    ch = data[turn % len(data)]
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

    return turn, rock_idx, x, y, fallen_count

if __name__ == '__main__':
    main()
