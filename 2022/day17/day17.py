#!/usr/bin/env python3
import itertools
import pickle
import string
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

ROCKS = (
    ['####'],
    '.#.\n###\n.#.'.split(),
    '..#\n..#\n###'.split(),
    ['#'] * 4,
    ['##', '##'],
)


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

    def height(self):
        return max(y + 1 for x, y in self.grid)

    @property
    def jet_idx(self):
        return self.turn % len(self.data)

    @property
    def key(self):
        return self.rock_idx, self.jet_idx


def drop_rock(state: State):
    '''Continues running the simulation until the current rock settles and a
    new rock is spawned.'''

    fallen_start = state.fallen_count
    while state.fallen_count == fallen_start:
        state = tick(state)
    return state


def rock_to_coords(x, y, rock):
    for r, row in enumerate(rock):
        for c, ch in enumerate(row):
            if ch == '#':
                yield x + c, y + (len(rock) - 1 - r)


def valid_pos(grid, newx, newy, rock):
    for rx, ry in rock_to_coords(newx, newy, rock):
        if ry < 0 or rx < 0 or rx > 6 or (rx, ry) in grid:
            return False
    return True


def pairwise_diff(lst):
    return list(b - a for a, b in zip(lst, lst[1:]))


def make_key(state: State):
    return (state.rock_idx, state.jet_idx)


def simfor(state: State, rocks_to_drop: int):
    '''Simulate dropping a number of rocks'''
    for _ in range(rocks_to_drop):
        state = drop_rock(state)
    return state


def print_grid(grid: dict[tuple[int, int], int], y_low=None, y_high=None):
    y_high = y_high or max(y for x, y in grid)
    y_low = y_low or 0
    y = y_high
    while y >= y_low:
        row = ('.#'[(x, y) in grid] for x in range(7))
        print(*row, sep='')
        y -= 1


def new_state(data: str):
    return State({}, data, turn=0, rock_idx=0, x=2, y=3, fallen_count=0)


def main():
    data = sys.stdin.read().strip()

    ans1 = simfor(new_state(data), 2022).height()
    print('part1:', ans1)

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

        print('Writing cache...')
        pickle.dump([state, heights, rock_counts], open(CACHE_FILE, 'wb'))
    else:
        print('Reading cache...')
        state, heights, rock_counts = pickle.load(open(CACHE_FILE, 'rb'))

    assert isinstance(state, State)
    assert isinstance(heights, dict)

    # Simulate until we have a suitable cycle (janky)
    state = new_state(data)
    while len(heights[state.key]
              ) < 3 or len(set(pairwise_diff(heights[state.key]))) > 1:
        state = drop_rock(state)

    # Note: Cycles occurs every 'cycle_pieces' pieces w/ a height of 'cycle_height'
    cycle_pieces = rock_counts[state.key][-1] - rock_counts[state.key][-2]
    cycle_height = heights[state.key][-1] - heights[state.key][-2]

    # Determine how many more cycles we can perform w/o going over
    rocks_left = 1000000000000 - state.fallen_count
    cycles_left, rocks_left = divmod(rocks_left, cycle_pieces)

    # Adjust height/count based on the number of cycles left
    current_rock_height = state.height() - 1
    current_rock_height += cycles_left * cycle_height
    current_rock_count = state.fallen_count + cycles_left * cycle_pieces

    # Drop the remaining rocks, then add the height delta
    y_before = state.last_piece_y or 0
    state = simfor(state, rocks_left)
    y_after = state.last_piece_y or 0

    # WARN: off-by one for part 2 of sample input. might be related to rock y-geometry (?)
    ans2 = current_rock_height + y_after - y_before
    print('part2:', ans2)

    assert ans1 == 3181
    assert ans2 == 1570434782634


def tick(state: State) -> State:
    '''
    Runs one tick of the simulation. Applies left/right jet stream,
    then drops rock down one tile. Grid only stores settled (not falling)
    rocks. rock_idx, x, and y correspond to the current falling rock.

    NOTE: This mutates the original state.grid.
    '''

    grid = state.grid  # mutable copy
    rock_idx = state.rock_idx
    turn = state.turn
    rock_idx = state.rock_idx
    x = state.x
    y = state.y
    fallen_count = state.fallen_count

    ch = state.data[state.jet_idx]
    rock = ROCKS[rock_idx]
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
        rock_idx %= len(ROCKS)
        fallen_count += 1

    return State(
        grid, state.data, turn + 1, rock_idx, x, y, fallen_count, last_piece_y
    )


if __name__ == '__main__':
    main()
