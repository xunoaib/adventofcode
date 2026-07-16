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


def find_adjacent_targets(attacker: Unit, units: list[Unit]):
    neighbor_tiles = {p for p in neighbors(*attacker.pos)}
    targets = [u for u in units if u.pos in neighbor_tiles and u.type != attacker.type]
    return sorted(targets, key=lambda u: (u.hp, u.pos))


def find_reachable_targets(src: Unit, units: list[Unit]):
    q: list[tuple[Point, int, tuple[Point, ...]]] = [(src.pos, 0, tuple())]
    routes: dict[Point, tuple[Point, ...]] = {src.pos: tuple()}

    while q:
        p, dist, path = q.pop(0)
        for n in open_neighbors(p, units):
            if n not in routes:
                routes[n] = path + (n,)
                q.append((n, dist + 1, path + (n,)))

    # filter to reachable targets only, sorted by distance
    enemy_neighbors = sorted(
        {
            pos
            for tar in units
            for pos in open_neighbors(tar.pos, units)
            if tar.type != src.type and pos in routes
        }
    )

    # return {pos: routes[pos] for pos in enemy_neighbors}
    # return [routes[pos] for pos in enemy_neighbors]
    final = [routes[pos] for pos in enemy_neighbors]
    return sorted(final, key=lambda route: (len(route), route[-1]))


def step(units):
    units.sort(key=lambda u: u.pos)

    # goblins = [u for u in units if u.type == 'G']
    # elves = [u for u in units if u.type == 'E']
    # type_units = [goblins, elves]

    for unit in units.copy():
        if targets := find_adjacent_targets(unit, units):
            print(unit, 'has targets')
        elif routes := find_reachable_targets(unit, units):
            print(unit, 'can reach', routes)
        else:
            print(unit, 'stuck')

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
