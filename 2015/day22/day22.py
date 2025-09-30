import re
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import override

SPELL_COSTS = {
    'missile': 53,
    'drain': 73,
    'shield': 113,
    'poison': 173,
    'recharge': 229,
}


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

    def __lt__(self, other: 'Game'):
        return self.boss.health < other.boss.health

    @override
    def __hash__(self):
        tup = tuple(
            sorted((e.timeleft, e.__class__.__name__) for e in self.effects)
        )
        return hash(
            (self.boss.health, self.player.health, self.player.mana) + tup
        )

    @override
    def __eq__(self, other: object):
        return hash(self) == hash(other)

    def missile(self):
        self.player.mana -= 53
        self.boss.health -= 4

    def drain(self):
        self.player.mana -= 73
        self.boss.health -= 2
        self.player.health += 2

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
                self.player.armor += 7
            elif isinstance(e, Poison):
                self.boss.health -= 3
            else:
                self.player.mana += 101
            e.timeleft -= 1
        self.prune_effects()

    def prune_effects(self):
        self.effects = [e for e in self.effects if e.timeleft > 0]

    def player_turn(self, action: str):
        if self.game_over:
            return
        self.apply_effects()
        if self.game_over:
            return

        if SPELL_COSTS[action] > self.player.mana:
            raise ValueError(f'Insufficient mana for {action}')

        actions = {
            'missile': self.missile,
            'drain': self.drain,
            'shield': self.shield,
            'poison': self.poison,
            'recharge': self.recharge,
        }

        actions[action]()

    def boss_turn(self):
        if self.game_over:
            return
        self.apply_effects()
        if self.game_over:
            return

        self.player.health -= max(1, self.boss.damage - self.player.armor)

    def castable_spells(self) -> list[str]:
        active_spells = {e.__class__.__name__.lower() for e in self.effects}
        spells: list[str] = []
        for spell, cost in SPELL_COSTS.items():
            if self.player.mana >= cost and spell not in active_spells:
                spells.append(spell)
        return spells

    def action(self, spell: str):
        game = deepcopy(self)
        game.player_turn(spell)
        game.boss_turn()
        return game

    @property
    def won(self):
        return self.boss.health <= 0

    @property
    def lost(self):
        return self.player.health <= 0

    @property
    def game_over(self):
        return self.won or self.lost


def part1(player: Player, boss: Boss):
    game = Game(player, boss)
    q = [(0, game)]
    seen: dict[Game, list[str]] = {game: []}

    while q:
        cost, game = heappop(q)
        if game.won:
            print(seen[game])
            return cost
        if game.lost:
            continue

        for spell in game.castable_spells():
            ncost = cost + SPELL_COSTS[spell]
            ngame = game.action(spell)
            if ngame not in seen:
                seen[ngame] = seen[game] + [spell]
                heappush(q, (ncost, ngame))


def main():

    # Sample input
    player = Player(10, 250)
    boss = Boss(13, 8)
    boss = Boss(14, 8)

    # Real input
    player = Player(50, 500)
    boss_hp, boss_dmg = map(int, re.findall(r'\d+', sys.stdin.read()))
    boss = Boss(boss_hp, boss_dmg)

    a1 = part1(player, boss)
    print('part1:', a1)


if __name__ == '__main__':
    main()
