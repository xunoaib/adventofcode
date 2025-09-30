import re
import sys
from dataclasses import dataclass, field

SPELLS = ['missile', 'drain', 'shield', 'poison', 'recharge']


@dataclass
class Boss:
    health: int
    damage: int
    effects: list['Effect'] = field(default_factory=list)


@dataclass
class Player:
    health: int
    mana: int
    armor: int = 0


@dataclass
class Shield:
    timeleft: int = 6


@dataclass
class Poison:
    timeleft: int = 6


@dataclass
class Recharge:
    timeleft: int = 5


Effect = Shield | Poison | Recharge


@dataclass
class Game:
    player: Player
    boss: Boss
    effects: list[Effect] = field(default_factory=list)

    def missile(self):
        self.player.mana -= 53
        self.boss.health -= 4

    def drain(self):
        self.player.mana -= 73
        self.player.health += 2
        self.boss.health -= 2

    def shield(self):
        self.player.mana -= 113
        self.effects.append(Shield())

    def poison(self):
        self.player.mana -= 173
        self.effects.append(Poison())

    def recharge(self):
        self.player.mana -= 229
        self.effects.append(Recharge())

    def apply_effects(self):
        self.player.armor = 0
        for e in self.effects:
            if isinstance(e, Shield):
                print('>> Shield active')
                self.player.armor += 7
            elif isinstance(e, Poison):
                print('>> Poison active')
                self.boss.health -= 3
            elif isinstance(e, Recharge):
                print('>> Recharge active')
                self.player.mana += 101
            e.timeleft -= 1
        self.effects = [e for e in self.effects if e.timeleft > 0]

    def player_step(self, action: str):
        self.apply_effects()
        print('-- Player turn --')
        print(
            f'Player has {self.player.health} hit points, {self.player.armor} armor, {self.player.mana} mana'
        )
        print(f'- Boss has {self.boss.health} hit points')

        actions = {
            'missile': self.missile,
            'drain': self.drain,
            'shield': self.shield,
            'poison': self.poison,
            'recharge': self.recharge,
        }

        print(f'Player casts {action}.')
        print()

        return actions[action]()

    def boss_step(self):
        self.apply_effects()
        print('-- Boss turn --')
        print(
            f'Player has {self.player.health} hit points, {self.player.armor} armor, {self.player.mana} mana'
        )
        print(f'- Boss has {self.boss.health} hit points')
        print(f'Boss attacks for {self.boss.damage} damage.')
        print()


def main():

    # Sample input
    player = Player(10, 250)
    boss = Boss(13, 8)

    # # Real input
    # player = Player(50, 500)
    # boss_hp, boss_dmg = map(int, re.findall(r'\d+', sys.stdin.read()))
    # boss = Boss(boss_hp, boss_dmg)

    game = Game(player, boss)

    game.player_step('poison')
    game.boss_step()

    game.player_step('missile')
    game.boss_step()


if __name__ == '__main__':
    main()
