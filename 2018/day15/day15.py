import sys
from dataclasses import dataclass

type Point = tuple[int, int]


@dataclass
class Unit:
    pos: Point
    type: str
    hp: int = 200
    atk: int = 3

    @property
    def is_goblin(self):
        return self.type == 'G'

    @property
    def is_elf(self):
        return self.type == 'E'


@dataclass
class State:
    units: list[Unit]

    @property
    def goblins(self):
        return [u for u in self.units if u.is_goblin]

    @property
    def elves(self):
        return [u for u in self.units if u.is_elf]


def neighbors(r, c):
    return {(r + dr, c + dc) for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]}


def open_neighbors(p: Point, units: list[Unit]):
    occupied = {u.pos for u in units}
    return {p for p in neighbors(*p) if p in WALKABLE and p not in occupied}


def reachable(src: Point, units: list[Unit]):
    q: list[tuple[Point, int, tuple[Point, ...]]] = [(src, 0, tuple())]
    routes: dict[Point, tuple[Point, ...]] = {src: tuple()}

    while q:
        p, dist, path = q.pop(0)
        for n in open_neighbors(p, units):
            if n not in routes:
                routes[n] = path + (n,)
                q.append((n, dist + 1, path + (n,)))

    return routes


def step(units):
    # # targets adjacent to elves (or goblins)
    # elf_targets = {n for p in state.elves for n in open_neighbors(p, state)}
    # goblin_targets = {n for p in state.goblins for n in open_neighbors(p, state)}

    units.sort(key=lambda u: u.pos)

    goblins = [u for u in units if u.type == 'G']
    elves = [u for u in units if u.type == 'E']

    type_units = [goblins, elves]

    # targets_of = {'E': [], 'E'

    for u in units:
        # 1. check for adjacent targets
        # if targets := {(n, u) for n,u in units.items()}
        print(u)

    # for p, goblin in sorted(state.goblins.items()):
    #     print(p, reachable(p, elf_targets, state))

    # # find elf routes to goblin targets
    # for p, elf in sorted(state.elves.items()):
    #     routes = reachable(p, state)
    #     routes = {k: v for k, v in routes.items() if k in goblin_targets}
    #     for k, v in routes.items():
    #         print(p, k, v)


def main():
    global WALKABLE

    aa = bb = None
    lines = sys.stdin.read().strip().split('\n')

    grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}
    WALKABLE = {p for p, v in grid.items() if v != '#'}
    units = [Unit(p, v) for p, v in grid.items() if v in 'EG']

    state = step(units)

    if locals().get('aa') is not None:
        print('part1:', aa)

    if locals().get('bb') is not None:
        print('part2:', bb)

    # assert aa == 0
    # assert bb == 0


if __name__ == '__main__':
    main()
