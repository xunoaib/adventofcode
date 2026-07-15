import sys
from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class Unit:
    type: str
    hp: int = 200
    atk: int = 3


@dataclass
class State:
    goblins: dict[tuple[int, int], Unit]
    elves: dict[tuple[int, int], Unit]


def neighbors(r, c):
    return {(r + dr, c + dc) for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]}


def open_neighbors(r, c, state: State):
    return {
        p
        for p in neighbors(r, c)
        if p in WALKABLE and p not in state.goblins | state.elves
    }


def step(state):
    new_state = State({}, {})

    for p, goblin in sorted(state.goblins.items()):
        print(goblin, open_neighbors(p[0], p[1], state))

    for p, elf in sorted(state.elves.items()):
        print(elf, open_neighbors(p[0], p[1], state))


def main():
    global WALKABLE

    aa = bb = None
    lines = sys.stdin.read().strip().split('\n')

    grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}
    WALKABLE = {p for p, v in grid.items() if v != '#'}
    goblins = {p: Unit('G') for p, v in grid.items() if v == 'G'}
    elves = {p: Unit('E') for p, v in grid.items() if v == 'E'}
    state = State(goblins, elves)

    state = step(state)

    if locals().get('aa') is not None:
        print('part1:', aa)

    if locals().get('bb') is not None:
        print('part2:', bb)

    # assert aa == 0
    # assert bb == 0


if __name__ == '__main__':
    main()
