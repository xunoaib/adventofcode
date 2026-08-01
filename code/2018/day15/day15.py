import sys
from copy import deepcopy
from dataclasses import dataclass
from itertools import count
from typing import override

type Point = tuple[int, int]


@dataclass
class Unit:
    pos: Point
    type: str
    hp: int = 200
    atk: int = 3

    @override
    def __repr__(self):
        return f'{self.type}({self.hp}, {self.pos})'


def display(units: list[Unit]):
    chars = {p: '.' for p in WALKABLE} | {u.pos: u.type for u in units}

    print()
    for r in range(ROWS):
        s = ''.join(chars.get((r, c), '#') for c in range(COLS))
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


def find_adjacent_target(attacker: Unit, units: list[Unit]):
    neighbor_tiles = {p for p in neighbors(*attacker.pos)}
    targets = [u for u in units if u.pos in neighbor_tiles and u.type != attacker.type]
    return min(targets, key=lambda u: (u.hp, u.pos), default=None)


def find_reachable_target(src: Unit, units: list[Unit]):
    # NOTE: works... very inefficiently!

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

        return {path for path in routes.values() if path[-1] in enemy_targets}

    # collect unique routes from all directions
    routes = set()
    for p in open_neighbors(src.pos, units):
        paths = find(p)
        for path in paths:
            routes.add(path)

    return min(
        routes,
        key=lambda route: (
            len(route),
            route[-1],
            route[0],
        ),
        default=None,
    )


def play_round(units: list[Unit]):
    units = units.copy()
    units.sort(key=lambda u: u.pos)

    def try_attack():
        if target := find_adjacent_target(unit, units):
            target.hp -= unit.atk
            if target.hp <= 0:
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
            unit.pos = route[0]
            try_attack()

    return units, True  # completed round


def play_game(units: list[Unit]):
    units = deepcopy(units)
    round = 0
    while len({u.type for u in units}) > 1:
        units, completed = play_round(units)
        round += completed
    return round, units


def part1(units: list[Unit]):
    print('Solving part 1...')
    round, units = play_game(units)
    return round * sum(u.hp for u in units)


def part2(units: list[Unit]):
    print('\nSolving part 2...')
    num_elves = sum(u.type == 'E' for u in units)
    original_units = deepcopy(units)

    for atk in count(4):
        print('testing atk =', atk)
        units = deepcopy(original_units)

        for u in units:
            if u.type == 'E':
                u.atk = atk

        round, units = play_game(units)

        if sum(u.type == 'E' for u in units) == num_elves:
            return round * sum(u.hp for u in units)


def main():
    global WALKABLE, ROWS, COLS

    lines = sys.stdin.read().strip().split('\n')
    grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}

    walls = {p for p, v in grid.items() if v == '#'}
    ROWS = 1 + max(r for r, _ in walls)
    COLS = 1 + max(c for _, c in walls)

    WALKABLE = {p for p, v in grid.items() if v != '#'}
    units = [Unit(p, v) for p, v in grid.items() if v in 'EG']

    print('part1:', a1 := part1(deepcopy(units)))
    print('part2:', a2 := part2(deepcopy(units)))

    assert a1 == 229950
    assert a2 == 54360


if __name__ == '__main__':
    main()
