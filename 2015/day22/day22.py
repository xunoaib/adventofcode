import re
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Literal, override

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
class Effect:
    name: str
    timeleft: int


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
        self.effects.append(Effect('shield', 6))

    def poison(self):
        self.player.mana -= 173
        self.effects.append(Effect('poison', 6))

    def recharge(self):
        self.player.mana -= 229
        self.effects.append(Effect('recharge', 5))

    def apply_effects(self):
        self.player.armor = 0
        for e in self.effects:
            match e.name:
                case 'shield':
                    self.player.armor += 7
                case 'poison':
                    self.boss.health -= 3
                case 'recharge':
                    self.player.mana += 101
                case _:
                    raise ValueError()
            e.timeleft -= 1
        self.effects = [e for e in self.effects if e.timeleft > 0]

    def player_turn(self, action: str):
        if not self.game_over:
            getattr(self, action)()
            self.mana_used += SPELL_COSTS[action]

    def boss_turn(self):
        if not self.game_over:
            self.player.health -= max(1, self.boss.damage - self.player.armor)

    def castable_spells(self) -> list[str]:
        active_spells = {e.__class__.__name__.lower() for e in self.effects}
        spells: list[str] = []
        for spell, cost in SPELL_COSTS.items():
            if self.player.mana >= cost and spell not in active_spells:
                spells.append(spell)
        return spells

    @property
    def player_won(self):
        return self.boss.health <= 0

    @property
    def player_lost(self):
        return self.player.health <= 0

    @property
    def game_over(self):
        return self.player_won or self.player_lost


def solve(game: Game, part: Literal[1, 2]):
    q = [game]
    seen: dict[Game, list[str]] = {game: []}

    while q:
        game = heappop(q)
        if game.player_won:
            print(seen[game])
            return game.mana_used

        for spell in game.castable_spells():

            g = deepcopy(game)
            g.player_turn(spell)
            g.apply_effects()
            g.boss_turn()
            g.apply_effects()

            if part == 2:
                g.player.health -= 1

            if not g.player_lost and g not in seen:
                seen[g] = seen[game] + [spell]
                heappush(q, g)


def main():

    boss_hp, boss_dmg = map(int, re.findall(r'\d+', sys.stdin.read()))
    boss = Boss(boss_hp, boss_dmg)
    player = Player(50, 500)
    game = Game(player, boss)

    a1 = solve(deepcopy(game), 1)
    a2 = solve(deepcopy(game), 2)

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 1269
    assert a2 == 1309


if __name__ == '__main__':
    main()
