import sys
from dataclasses import dataclass

type Point = tuple[int, int]


@dataclass
class Unit:
    type: str
    hp: int = 200
    atk: int = 3


@dataclass
class State:
    goblins: dict[Point, Unit]
    elves: dict[Point, Unit]


def neighbors(r, c):
    return {(r + dr, c + dc) for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]}


def open_neighbors(p: Point, state: State):
    return {
        p
        for p in neighbors(*p)
        if p in WALKABLE and p not in state.goblins | state.elves
    }


def reachable(src: Point, state: State):
    q: list[tuple[Point, int, tuple[Point, ...]]] = [(src, 0, tuple())]
    routes: dict[Point, tuple[Point, ...]] = {src: tuple()}

    while q:
        p, dist, path = q.pop(0)
        for n in open_neighbors(p, state):
            if n not in routes:
                routes[n] = path + (n,)
                q.append((n, dist + 1, path + (n,)))

    return routes


def step(state):
    new_state = State({}, {})

    # targets adjacent to elves (or goblins)
    elf_targets = {n for p in state.elves for n in open_neighbors(p, state)}
    goblin_targets = {n for p in state.goblins for n in open_neighbors(p, state)}

    print('E', elf_targets)
    print('G', goblin_targets)
    print()

    # for p, goblin in sorted(state.goblins.items()):
    #     print(p, reachable(p, elf_targets, state))

    for p, elf in sorted(state.elves.items()):
        routes = reachable(p, state)
        routes = {k: v for k, v in routes.items() if k in goblin_targets}
        for k, v in routes.items():
            print(p, k, v)


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
