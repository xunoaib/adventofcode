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

    def __repr__(self):
        n = ['Goblin', 'Elf'][self.is_elf]
        return f'{n}(pos={self.pos}, hp={self.hp})'


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

    final = [routes[pos] for pos in enemy_neighbors]
    return sorted(final, key=lambda route: (len(route), route[-1]))


def play_round(units: list[Unit]):
    print('\n==== playing round ====\n')
    units = units.copy()
    units.sort(key=lambda u: u.pos)

    for unit in units.copy():
        if unit not in units:
            continue

        if targets := find_adjacent_targets(unit, units):
            target = targets[0]
            print('🩸', unit, 'attacked', target)
            target.hp -= unit.atk
            if target.hp <= 0:
                print('💀', unit, 'killed', target)
                units.remove(target)

        elif routes := find_reachable_targets(unit, units):
            newpos = routes[0][0]
            print('🦶', unit, 'moved to', newpos)
            unit.pos = newpos

        else:
            print('🛑', unit, 'stuck')

    return units


def main():
    global WALKABLE

    aa = bb = None
    lines = sys.stdin.read().strip().split('\n')

    grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}
    WALKABLE = {p for p, v in grid.items() if v != '#'}
    units = [Unit(p, v) for p, v in grid.items() if v in 'EG']

    while True:
        units = play_round(units)
        if len({u.type for u in units}) <= 1:
            break

    if locals().get('aa') is not None:
        print('part1:', aa)

    if locals().get('bb') is not None:
        print('part2:', bb)

    # assert aa == 0
    # assert bb == 0


if __name__ == '__main__':
    main()
