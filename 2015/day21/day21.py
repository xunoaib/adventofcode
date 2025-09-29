import re
import sys
from dataclasses import dataclass, field


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


@dataclass
class Item:
    name: str
    type: str
    stats: Stats

    def __add__(self, other: 'Item'):
        return self.stats + other.stats

    def __radd__(self, other):
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

    def stats(self):
        return sum(self.items)


@dataclass
class Player:
    inventory: Inventory
    health: int

    def attack(self):
        pass


class Game:

    def __init__(self):
        self.health = health
        self.boss_health = boss_health


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


def main():
    items = parse_shop_items()
    inv = Inventory()

    for i in items:
        print(i)

    inv.items.append(items[0])
    print(inv.stats())


if __name__ == '__main__':
    main()
