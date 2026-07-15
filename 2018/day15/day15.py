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


def open_neighbors(p: tuple[int, int], state: State):
    return {
        p
        for p in neighbors(*p)
        if p in WALKABLE and p not in state.goblins | state.elves
    }


def reachable(src: tuple[int, int], pois, state: State):
    q = [src]
    seen = {q[0]}
    while q:
        p = q.pop()
        for n in open_neighbors(p, state):
            if n not in seen:
                seen.add(n)
                q.append(n)
    return set(pois) & seen


def step(state):
    new_state = State({}, {})

    # targets adjacent to elves (or goblins)
    elf_targets = {n for p in state.elves for n in open_neighbors(p, state)}
    goblin_targets = {n for p in state.goblins for n in open_neighbors(p, state)}

    print(elf_targets)
    print(goblin_targets)

    for p, goblin in sorted(state.goblins.items()):
        print(reachable(p, elf_targets, state))

    for p, elf in sorted(state.elves.items()):
        print(reachable(p, goblin_targets, state))


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
