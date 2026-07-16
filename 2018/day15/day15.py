import sys
from copy import deepcopy
from dataclasses import dataclass
from itertools import count

type Point = tuple[int, int]


def debug(*args):
    if '-v' in sys.argv:
        print(*args)


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
        n = 'GE'[self.is_elf]
        return f'{n}({self.hp}, {self.pos})'


@dataclass
class State:
    units: list[Unit]

    @property
    def goblins(self):
        return [u for u in self.units if u.is_goblin]

    @property
    def elves(self):
        return [u for u in self.units if u.is_elf]


def display(units: list[Unit]):
    ROWS = 1 + max(r for r, c in WALLS)
    COLS = 1 + max(c for r, c in WALLS)

    chars = {p: '#' for p in WALLS}
    chars |= {p: '.' for p in WALKABLE}
    chars |= {u.pos: 'GE'[u.is_elf] for u in units}

    print()
    for r in range(ROWS):
        s = ''.join(chars[r, c] for c in range(COLS))
        hps = ', '.join(
            f'{u.type}({u.hp})' for c in range(COLS) for u in units if u.pos == (r, c)
        )
        if hps:
            hps = '  ' + hps
        print(s, hps)
    print()


def neighbors(r, c):
    return {(r + dr, c + dc) for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]}


def open_neighbors(p: Point, units: list[Unit]):
    occupied = {u.pos for u in units}
    return {p for p in neighbors(*p) if p in WALKABLE and p not in occupied}


def find_adjacent_targets(attacker: Unit, units: list[Unit]):
    neighbor_tiles = {p for p in neighbors(*attacker.pos)}
    targets = [u for u in units if u.pos in neighbor_tiles and u.type != attacker.type]
    return sorted(targets, key=lambda u: (u.hp, u.pos))


def find_reachable_target(src: Unit, units: list[Unit]):

    enemy_targets = {
        pos
        for tar in units
        for pos in open_neighbors(tar.pos, units)
        if tar.type != src.type
    }

    def find(src: Point):
        q: list[tuple[Point, int, tuple[Point, ...]]] = [(src, 0, (src,))]
        routes: dict[Point, tuple[Point, ...]] = {src: (src,)}

        while q:
            p, dist, path = q.pop(0)
            for n in open_neighbors(p, units):
                if n not in routes:
                    routes[n] = path + (n,)
                    q.append((n, dist + 1, path + (n,)))

        return {path for p, path in routes.items() if path[-1] in enemy_targets}

    # collect unique routes from all directions
    routes = set()
    for p in open_neighbors(src.pos, units):
        paths = find(p)
        for path in paths:
            routes.add(path)

    routes = sorted(
        routes,
        key=lambda route: (
            len(route),
            # [manhattan_dist(p, route[-1]) for p in route],
            # route,
            route[-1],
            route[0],
        ),
    )

    return routes[0] if routes else None


def manhattan_dist(a: Point, b: Point):
    return sum(abs(x - y) for x, y in zip(a, b))


def play_round(units: list[Unit]):
    units = units.copy()
    units.sort(key=lambda u: u.pos)

    def try_attack():
        if targets := find_adjacent_targets(unit, units):
            target = targets[0]
            debug('🩸', unit, 'attacks', target)
            target.hp -= unit.atk
            if target.hp <= 0:
                debug('💀', unit, 'killed', target)
                units.remove(target)
            return True
        return False

    for unit in units.copy():
        # check if game is over
        if len({u.type for u in units}) <= 1:
            return units, False  # didnt complete round

        if unit not in units:
            continue

        if try_attack():
            continue

        if route := find_reachable_target(unit, units):
            newpos = route[0]
            debug('🏃', unit, 'moving to', newpos)
            unit.pos = newpos
            try_attack()
        else:
            debug('⏳', unit, 'stuck')

    return units, True  # completed round


def play_game(units: list[Unit]):
    units = deepcopy(units)
    round = 0
    while True:
        # print(f'\n==== round {round} ====\n')
        units, completed = play_round(units)
        # debug()
        # display(units)
        round += completed
        if len({u.type for u in units}) <= 1:
            break
    return round, units


def part1(units: list[Unit]):
    round, units = play_game(units)
    s = sum(u.hp for u in units)
    aa = round * s
    print(round, '*', s, '=', aa)
    return aa


def part2(units: list[Unit]):

    display(units)

    num_elves = sum(u.type == 'E' for u in units)
    original_units = deepcopy(units)

    for atk in count(4):
        print('testing atk =', atk)
        units = deepcopy(original_units)
        for u in units:
            if u.is_elf:
                u.atk = atk

        round, units = play_game(units)

        if sum(u.type == 'E' for u in units) == num_elves:
            s = sum(u.hp for u in units)
            aa = round * s
            print('attack =', atk)
            print(round, '*', s, '=', aa)
            display(units)
            return aa


def main():
    global WALKABLE, WALLS

    aa = bb = None
    lines = sys.stdin.read().strip().split('\n')

    grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}
    WALLS = {p for p, v in grid.items() if v == '#'}
    WALKABLE = {p for p, v in grid.items() if v != '#'}
    units = [Unit(p, v) for p, v in grid.items() if v in 'EG']

    # aa = part1(deepcopy(units))
    bb = part2(deepcopy(units))

    if locals().get('aa') is not None:
        print('part1:', aa)

    if locals().get('bb') is not None:
        print('part2:', bb)

    # assert aa == 229950
    # assert bb == 0


if __name__ == '__main__':
    main()
