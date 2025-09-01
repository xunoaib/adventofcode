#!/usr/bin/env python3
import itertools
import pickle
import string
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

rocks = [
    ['####'],
    '.#.\n###\n.#.'.split(),
    '..#\n..#\n###'.split(),
    ['#'] * 4,
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


def pairwise_diff(lst):
    return list(b - a for a, b in zip(lst, lst[1:]))


def make_key(state: 'State'):
    return (state.rock_idx, state.jet_idx)


def simfor(state: 'State', steps: int):
    for _ in range(steps):
        state = drop_rock(state)
    return state


def print_grid(grid: dict[tuple[int, int], int], y_low=None, y_high=None):

    y_high = y_high or max(y for x, y in grid)
    y_low = y_low or 0

    y = y_high
    while y >= y_low:
        # row = (str(grid.get((x, y), '.')).rjust(5) for x in range(7))
        row = ('.#'[(x, y) in grid] for x in range(7))
        print(*row, sep='')
        y -= 1

    return

    print('')
    if not grid:
        print('nothing')
        return

    max_height = max(y for _, y in grid)
    min_height = min(y for _, y in grid)
    print(f'y: {min_height} to {max_height}')

    if y_high is None:
        yend = max_height

    if y_low is None:
        ystart = min_height

    print(f'printing from {yend} to {ystart}')

    for y in range(yend, ystart, -1):
        for x in range(8):
            ch = grid.get((x, y), '.')
            if isinstance(ch, int):
                ch = string.ascii_letters[ch % len(string.ascii_letters)]
            print(ch, end='')
        print()


def find_largest_repeat(grid):
    ymax = max(y for _, y in grid)
    rows = [
        tuple(x for x in range(MAX_X + 1) if (x, y) in grid)
        for y in range(ymax + 1)
    ]

    best_total = 0
    for ystart in range(3100, ymax):  # save time by starting at 3100
        height_left = ymax + 1 - ystart
        for length in range(
            1, height_left // 2
        ):  # when trying to place 2 blocks, their max height will be 1/2 the space left
            # find the total number of duplicated blocks of height 'length' starting from 'ystart'
            repeats = 0
            for num_repeats in range(1, height_left // length):
                if not compare_blocks(
                    rows, ystart, ystart + num_repeats * length, length
                ):
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

    return (0, ) * 4


def compare_blocks(rows, ystart1, ystart2, height):
    """Check if two regions of the given height at ystart1 and ystart2 are equal"""
    if ystart2 < ystart1:
        ystart1, ystart2 = ystart2, ystart1

    for yoff in range(height):
        if rows[ystart1 + yoff] != rows[ystart2 + yoff]:
            return False
    return True


def new_state(data: str):
    return State({}, data, turn=0, rock_idx=0, x=2, y=3, fallen_count=0)


def main():
    data = sys.stdin.read().strip()

    if len(data) == 40:
        print('Detected sample input')
        CACHE_FILE = Path('cache_sample.pkl')
    else:
        print('Detected real input')
        CACHE_FILE = Path('cache_actual.pkl')

    state = new_state(data)
    heights = defaultdict(list)
    rock_counts = defaultdict(list)

    if not CACHE_FILE.exists():
        # Hopefully simulate enough dropped rocks to capture a cycle
        num_rocks = 10000
        for i in range(1, num_rocks + 1):
            # Cycles can only occur at the same key: (rock_idx, jet_idx)
            key = state.key
            state = drop_rock(state)
            heights[key].append(state.last_piece_y)
            rock_counts[key].append(state.fallen_count)

            if i == 2022:
                print('part1:', state.max_y())

        print('Writing cache...')
        pickle.dump([state, heights, rock_counts], open(CACHE_FILE, 'wb'))
    else:
        print('Reading cache...')
        state, heights, rock_counts = pickle.load(open(CACHE_FILE, 'rb'))

    assert isinstance(state, State)
    assert isinstance(heights, dict)

    # Simulate until we have dupes
    state = new_state(data)
    while len(heights[state.key]
              ) < 3 or len(set(pairwise_diff(heights[state.key]))) > 1:
        state = drop_rock(state)

    # Note: Cycles occurs every 'cycle_pieces' pieces w/ a height of 'cycle_height'

    cycle_height = heights[state.key][-1] - heights[state.key][-2]
    cycle_pieces = rock_counts[state.key][-1] - rock_counts[state.key][-2]
    # current_rock_count = rock_counts[state.key][-1]

    print('cycle_height:', cycle_height)
    print('cycle_pieces:', cycle_pieces)
    # print('current_rock_count:', current_rock_count)

    # # Confirm cycle produces the same key
    # print('key before:', state.key)
    # state = simfor(state, cycle_pieces)
    # print('key after:', state.key)

    # y_before = state.max_y
    # state = simfor(state, cycle_pieces)
    # y_after = state.max_y

    # Determine how many more cycles we can perform w/o going over
    rocks_left = 1000000000000 - state.fallen_count
    cycles_left = int(rocks_left / cycle_pieces)

    print('rocks_left:', rocks_left)
    print('cycles_left:', cycles_left)

    # Adjust height/count based on cycles left
    current_rock_height = state.max_y() - 1  # heights[k][-1]
    current_rock_height += cycles_left * cycle_height
    current_rock_count = state.fallen_count + cycles_left * cycle_pieces

    rocks_left -= cycles_left * cycle_pieces

    print('rocks_left:', rocks_left)
    print('cycles_left:', cycles_left)

    y_before = state.last_piece_y or 0
    for _ in range(rocks_left):
        state = drop_rock(state)
    y_after = state.last_piece_y or 0
    y_diff = y_after - y_before
    print('y_diff', y_diff)

    ans2 = current_rock_height + y_diff
    print('part2:', ans2)
    assert ans2 == 1570434782634


@dataclass
class State:
    grid: dict
    data: str
    turn: int
    rock_idx: int
    x: int
    y: int
    fallen_count: int
    last_piece_y: int | None = None

    def max_y(self):
        return max(y + 1 for x, y in self.grid)

    @property
    def jet_idx(self):
        return self.turn % len(self.data)

    @property
    def key(self):
        return self.rock_idx, self.jet_idx


def tick(state: State):
    '''
    Runs one tick of the simulation. Applies left/right jet stream,
    then drops rock down one tile. Grid only stores settled (not falling)
    rocks. rock_idx, x, and y correspond to the current falling rock.
    '''

    grid = state.grid  # NOTE: reference
    rock_idx = state.rock_idx
    turn = state.turn
    rock_idx = state.rock_idx
    x = state.x
    y = state.y
    fallen_count = state.fallen_count

    ch = state.data[state.jet_idx]
    rock = rocks[rock_idx]
    xoff = 1 if ch == '>' else -1  # horiz direction to shift based on jet stream
    newx = max(0, min(6, x + xoff))  # clamp x position to game area
    newy = y - 1  # drop rock down
    last_piece_y = None

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
            grid[coord] = fallen_count

        last_piece_y = y

        # spawn new rock
        x = 2
        y = 4 + max(y for _, y in grid)
        rock_idx += 1
        rock_idx %= len(rocks)
        fallen_count += 1

    return State(
        grid, state.data, turn + 1, rock_idx, x, y, fallen_count, last_piece_y
    )


def drop_rock(state: State):
    '''Continues running the simulation until the current rock settles and a
    new rock is spawned.'''

    fallen_start = state.fallen_count
    while state.fallen_count == fallen_start:
        state = tick(state)
    return state


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
