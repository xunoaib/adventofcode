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
    ymax = max(y for _,y in grid)
    rows = [
        tuple(x for x in range(MAX_X + 1) if (x,y) in grid)
        for y in range(ymax + 1)
    ]

    best_total = 0
    for ystart in range(3100, ymax):  # save time by starting at 3100
        height_left = ymax + 1 - ystart
        for length in range(1, height_left // 2):  # when trying to place 2 blocks, their max height will be 1/2 the space left
            # find the total number of duplicated blocks of height 'length' starting from 'ystart'
            repeats = 0
            for num_repeats in range(1, height_left // length):
                if not compare_blocks(rows, ystart, ystart + num_repeats * length, length):
                    break
                else:
                    repeats = num_repeats

            total = repeats * length
            if total > best_total:
                # print(f'{ystart=}, {length=}, {repeats=}, {total=}')
                best_total = total

            if best_total > 1000:
                leftover = ymax - (ystart + best_total)
                # print('unmatched at the top:', leftover)
                return ystart, length, repeats, leftover

    return (0,) * 4

def compare_blocks(rows, ystart1, ystart2, height):
    """Check if two regions of the given height at ystart1 and ystart2 are equal"""
    if ystart2 < ystart1:
        ystart1, ystart2 = ystart2, ystart1

    for yoff in range(height):
        if rows[ystart1 + yoff] != rows[ystart2 + yoff]:
            return False
    return True

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
            # assert y - 3 == 3181
            break

    # for _ in range(30000):
    for _ in range(20000):
        turn, rock_idx, x, y, fallen_count = tick(grid, data, turn, rock_idx, x, y, fallen_count)

    # 1. establish a baseline by dropping rocks until the repeated pattern count increases.
    # 2. then drop more rocks until the repeat count increases again.
    # 3. then count the number of dropped rocks between these events for the final calculation.

    ret0 = ystart0, length0, repeats0, leftover0 = find_largest_repeat(grid)

    # 1. drop rocks until a new repeat occurs
    repeats1 = repeats0
    while repeats1 == repeats0:
        turn, rock_idx, x, y, fallen_count = tick(grid, data, turn, rock_idx, x, y, fallen_count)
        ystart1, length1, repeats1, _ = find_largest_repeat(grid)

    # drop_rock(grid, data, turn, rock_idx, x, y, fallen_count)

    fallen_count1 = fallen_count
    ymax1 = max(y for _,y in grid)

    # # 2. drop rocks until a second repeat occurs
    # repeats2 = repeats1
    # while repeats2 == repeats1:
    #     turn, rock_idx, x, y, fallen_count = tick(grid, data, turn, rock_idx, x, y, fallen_count)
    #     ystart2, length2, repeats2, _ = find_largest_repeat(grid)
    fallen_count2 = fallen_count
    ymax2 = max(y for _,y in grid)

    # number of rocks needed to cause a repeated pattern
    rock_repeat_interval = fallen_count2 - fallen_count1

    # the height increase of a single repetition
    single_repeat_height = ymax2 - ymax1

    print(find_largest_repeat(grid))

    print(fallen_count)
    print(rock_repeat_interval)

    if not rock_repeat_interval:
        print('woops, zero interval')
        exit(0)

    repeats_left = (1000000000000 - fallen_count) // rock_repeat_interval
    total_height = ymax2 + (single_repeat_height) * repeats_left

    print(f'{rock_repeat_interval=}')
    print(f'{single_repeat_height=}')
    print(f'{ymax2=}')
    print(f'{repeats_left=}')
    print(f'{total_height=}')
    print('diff:', total_height - 1514285714288)

    # # test interval (drop 6 sets of 5 rocks)
    # for _ in range(6):
    #     for _ in range(repeat_rock_interval):
    #         turn, rock_idx, x, y, fallen_count = drop_rock(grid, data, turn, rock_idx, x, y, fallen_count)

    print(f'{ystart0=}, {length0=}, {repeats0=}, {leftover0=}')

def tick(grid, data, turn, rock_idx, x, y, fallen_count):
    '''
    Runs one tick of the simulation. Applies left/right jet stream,
    then drops rock down one tile. Grid only stores settled (not falling)
    rocks. rock_idx, x, and y correspond to the current falling rock.
    '''
    ch = data[turn % len(data)]
    rock = rocks[rock_idx]
    xoff = 1 if ch == '>' else -1   # horiz direction to shift based on jet stream
    newx = max(0, min(6, x + xoff)) # clamp x position to game area
    newy = y - 1  # drop rock down

    # validate and apply horizontal movement
    if valid_pos(grid, newx, y, rock):
        x = newx

    # validate and apply vertical movement
    if valid_pos(grid, x, newy, rock):
        y = newy

    # rock has settled, so update the grid
    else:
        coords = list(rock_to_coords(x, y, rock))
        for coord in coords:
            grid[coord] = '#'

        # spawn new rock
        x = 2
        y = 4 + max(y for _,y in grid)
        rock_idx += 1
        rock_idx %= len(rocks)
        fallen_count += 1

    return turn, rock_idx, x, y, fallen_count

def drop_rock(grid, data, turn, rock_idx, x, y, fallen_count):
    '''Continues running the simulation until the current rock settles and a
    new rock is spawned.'''

    fallen_start = fallen_count
    while fallen_count == fallen_start:
        turn, rock_idx, x, y, fallen_count = tick(grid, data, turn, rock_idx, x, y, fallen_count)
    return turn, rock_idx, x, y, fallen_count

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
