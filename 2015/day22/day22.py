import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import override


@dataclass
class Boss:
    health: int
    damage: int
    effects: list['Effect'] = field(default_factory=list)


@dataclass
class Player:
    health: int
    mana: int


class Effect:
    cost: int = 0
    timeleft: int = 0

    def tick(self, player: Player, boss: Boss):
        self.timeleft -= 1


class MagicMissile(Effect):
    cost: int = 53
    timeleft: int = 0

    def apply(self, player: Player, boss: Boss):
        print('Applying missile')
        player.mana -= self.cost
        boss.health -= 4
        self.timeleft -= 1


class Drain(Effect):
    cost: int = 73
    timeleft: int = 0

    def apply(self, player: Player, boss: Boss):
        print('Applying drain')
        player.mana -= self.cost
        player.health += 2
        boss.health -= 2


def main():
    boss_hp, boss_dmg = map(int, re.findall(r'\d+', sys.stdin.read()))

    player = Player(50, 500)
    boss = Boss(boss_hp, boss_dmg)

    a = (player, boss)

    MagicMissile().apply(*a)
    Drain().apply(*a)

    print(boss)


if __name__ == '__main__':
    main()
