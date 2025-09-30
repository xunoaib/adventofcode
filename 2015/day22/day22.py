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
    mana_used: int = 0
    effects: list[Effect] = field(default_factory=list)

    def __lt__(self, other: 'Game'):
        return self.mana_used < other.mana_used

    @override
    def __hash__(self):
        return hash(
            (
                self.boss.health,
                self.player.health,
                self.player.mana,
                # self.mana_used,
            ) + tuple(
                sorted(
                    (e.timeleft, e.__class__.__name__) for e in self.effects
                )
            )
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
            else:  # Recharge
                self.player.mana += 101
            e.timeleft -= 1
        self.effects = [e for e in self.effects if e.timeleft > 0]

    def print_status(self, turn: str):
        print(f'-- {turn} turn --')
        print(
            f'- Player has {self.player.health} hit points, {self.player.armor} armor, {self.player.mana} mana'
        )
        print(f'- Boss has {self.boss.health} hit points')

    def player_turn(self, action: str):
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
        self.mana_used += SPELL_COSTS[action]

    def boss_turn(self):
        if self.game_over:
            return
        self.player.health -= max(1, self.boss.damage - self.player.armor)

    def castable_spells(self) -> list[str]:
        active_spells = {e.__class__.__name__.lower(): e for e in self.effects}
        spells: list[str] = []
        for spell, cost in SPELL_COSTS.items():
            if self.player.mana >= cost and spell not in active_spells:
                spells.append(spell)
        return spells

    def action(self, spell: str):

        # assert spell not in {
        #     e.__class__.__name__.lower()
        #     for e in self.effects
        # }

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

    @property
    def game_active(self):
        return not self.game_over


def part1(player: Player, boss: Boss):
    game = Game(player, boss)
    q = [game]
    seen: dict[Game, list[str]] = {game: []}

    best = float('inf')

    while q:
        game = heappop(q)
        if game.won:
            return game.mana_used

        for spell in game.castable_spells():

            g = deepcopy(game)
            g.player_turn(spell)
            g.apply_effects()
            g.boss_turn()
            g.apply_effects()

            if not g.lost and g not in seen:
                seen[g] = seen[game] + [spell]
                heappush(q, g)

    return best


def main():

    player = Player(50, 500)
    boss_hp, boss_dmg = map(int, re.findall(r'\d+', sys.stdin.read()))
    boss = Boss(boss_hp, boss_dmg)

    if '-s' in sys.argv:
        player = Player(10, 250)
        boss = Boss(13, 8)  # 226

    if '-t' in sys.argv:
        player = Player(10, 250)
        boss = Boss(14, 8)  # 641

    a1 = part1(player, boss)
    print('part1:', a1)


if __name__ == '__main__':
    main()
