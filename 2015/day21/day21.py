import re
import sys
from dataclasses import dataclass, field
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
        a = (self.cost, self.damage, other.armor)
        b = (other.cost, other.damage, other.armor)
        return a < b


@dataclass
class Item:
    name: str
    type: str
    stats: Stats

    def __add__(self, other: 'Item'):
        return self.stats + other.stats

    def __radd__(self, other: 'Literal[0] | Item'):
        if other == 0:
            return self.stats
        return self.__add__(other)


@dataclass
class Inventory:
    items: list[Item] = field(default_factory=list)

    def can_buy(self, other: Item):
        if other.type == 'weapon':
            return all(item.type != 'weapon' for item in self.items)
        elif other.type == 'armor':
            return all(item.type != 'armor' for item in self.items)
        elif other.type == 'ring':
            return sum(item.type == 'ring' for item in self.items) < 2

    def stats(self) -> Stats:
        s = Stats(0, 0, 0)
        for i in self.items:
            s = s + i.stats
        return s


@dataclass
class Player:
    health: int
    inventory: Inventory = field(default_factory=Inventory)

    @property
    def stats(self) -> Stats:
        return self.inventory.stats()

    @property
    def armor(self):
        return self.stats.armor

    @property
    def damage(self):
        return self.stats.damage

    def attack(self, other: 'Player'):
        other.health -= max(1, self.damage - other.armor)


class Game:

    def __init__(self, players: list[Player]):
        self.players = players


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


def parse_shop_items() -> list[Item]:
    items = []
    itype = ''
    for line in SHOP_STR.strip().splitlines():
        if ':' in line:
            itype = line.split(':')[0].rstrip('s').lower()
        elif m := re.match(r'^(.*?)\s+(\d+)\s+(\d+)\s+(\d+)$', line):
            name, *vals = m.groups()
            items.append(Item(name, itype, Stats(*map(int, vals))))
    return items


def combinations_up_to(items: list[Item], max_r):
    for r in range(0, max_r + 1):
        yield from combinations(items, r=r)


def iter_inventories():
    shop = parse_shop_items()
    rings = [i for i in shop if i.type == 'ring']
    armors = [i for i in shop if i.type == 'armor']
    weapons = [i for i in shop if i.type == 'weapon']

    for rcomb in combinations_up_to(rings, 2):
        for wcomb in combinations_up_to(weapons, 1):
            for acomb in combinations_up_to(armors, 1):
                yield rcomb + wcomb + acomb


def main():
    data = sys.stdin.read()
    boss_hp, boss_damage, boss_armor = map(int, re.findall(r'\d+', data))

    options = []
    for idx, items in enumerate(iter_inventories()):
        s = sum([i.stats for i in items] + [Stats(0, 0, 0)])
        options.append((s, idx, items))

    options.sort()

    for stats, _, items in options:
        # print(totcost, items)
        # stats = sum(item.stats for item in items)
        # print(totcost, stats)
        print(stats, s)


if __name__ == '__main__':
    main()
