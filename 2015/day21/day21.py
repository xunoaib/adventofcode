import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Literal


@dataclass
class Stats:
    cost: int
    damage: int
    armor: int

    def __add__(self, other: 'Stats'):
        return Stats(
            self.cost + other.cost,
            self.damage + other.damage,
            self.armor + other.armor,
        )

    def __radd__(self, other: 'Literal[0] | Stats') -> 'Stats':
        if other == 0:
            return self
        return self + other

    def __lt__(self, other: 'Stats'):
        return self.cost < other.cost


@dataclass
class Player:
    health: int
    stats: Stats

    def attack(self, other: 'Player'):
        other.health -= max(1, self.stats.damage - other.stats.armor)

    @property
    def alive(self):
        return self.health > 0


SHOP_STR = '''
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
'''


def parse_shop_items() -> dict[str, list[Stats]]:
    items = defaultdict(list)
    itype = ''
    for line in SHOP_STR.strip().splitlines():
        if ':' in line:
            itype = line.split(':')[0].rstrip('s').lower()
        elif m := re.match(r'^(.*?)\s+(\d+)\s+(\d+)\s+(\d+)$', line):
            _name, *vals = m.groups()
            items[itype].append(Stats(*map(int, vals)))
    return dict(items)


def range_combinations(items: list[Stats], mininum: int, maximum: int):
    for r in range(mininum, maximum + 1):
        yield from combinations(items, r=r)


def gear_combinations():
    shop = parse_shop_items()
    empty = (Stats(0, 0, 0), )

    for wcomb in range_combinations(shop['weapon'], 1, 1):
        for acomb in range_combinations(shop['armor'], 0, 1):
            for rcomb in range_combinations(shop['ring'], 0, 2):
                yield (wcomb + acomb + rcomb) or empty


def hero_wins(hero: Player, boss: Player):
    while hero.alive and boss.alive:
        hero.attack(boss)
        if not boss.alive:
            return True
        boss.attack(hero)
    return hero.alive


def main():
    data = sys.stdin.read()
    boss_hp, boss_damage, boss_armor = map(int, re.findall(r'\d+', data))
    boss_stats = Stats(0, boss_damage, boss_armor)

    options = []
    for idx, items in enumerate(gear_combinations()):
        options.append((sum(items), idx, items))
    options.sort()

    a1 = a2 = None

    for stats, _, items in options:
        hero = Player(100, stats)
        boss = Player(boss_hp, boss_stats)

        if not hero_wins(hero, boss):
            a2 = stats.cost
        elif a1 is None:
            a1 = stats.cost

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 78
    assert a2 == 148


if __name__ == '__main__':
    main()
