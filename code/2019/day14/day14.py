import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from z3 import ArithRef, Int, Optimize, Solver


@dataclass(frozen=True)
class Resource:
    name: str
    amount: int


@dataclass(frozen=True)
class Recipe:
    inputs: list[Resource]
    output: Resource


recipes: list[Recipe] = []
recipe_lookup: dict[str, Recipe] = {}

for line in sys.stdin:
    left, right = line.strip().split(' => ')

    counts = []
    for g in left.split(', ') + [right]:
        n, s = g.split()
        counts.append((s, int(n)))

    *inputs, output = [Resource(*c) for c in counts]
    recipe_lookup[output.name] = recipe = Recipe(inputs, output)
    recipes.append(recipe)

# Allow creating one ORE at any time
recipe_lookup['ORE'] = recipe = Recipe([], Resource('ORE', 1))
recipes.append(recipe)


@dataclass(frozen=True)
class ZReaction:
    name: str

    @property
    def reaction(self):
        return recipe_lookup[self.name]

    @property
    def zconsumed(self):
        return {
            inp.name: inp.amount * rcounts[self.name]
            for inp in self.reaction.inputs
        }

    @property
    def zproduced(self):
        return self.reaction.output.amount * rcounts[self.name]


names = [r.output.name for r in recipes]

# Create variables representing the number of times each reaction occurs
rcounts = {r.output.name: Int(f'rcount_{r.output.name}') for r in recipes}

# Represent total counts of each resource (ie: produced - consumed)
produced: dict[str, ArithRef | int] = {n: 0 for n in names}
consumed: dict[str, ArithRef | int] = {n: 0 for n in names}

for r in recipes:
    zreaction = ZReaction(r.output.name)

    # Add outputs
    produced[zreaction.name] += zreaction.zproduced

    # Subtract inputs
    for name, expr in zreaction.zconsumed.items():
        consumed[name] += expr

s = Optimize()

# Ensure resource consumption never exceeds production
for name in names:
    s.add(produced[name] - consumed[name] >= 0)

# Ensure reaction counts are positive
for rcount in rcounts.values():
    s.add(rcount >= 0)


def part1(s: Optimize):
    s.push()
    s.add(produced['FUEL'] == 1)
    s.minimize(rcounts['ORE'])
    s.check()

    if m := s.model():
        s.pop()
        return m.evaluate(produced['ORE'])

    raise ValueError('Part 1 unsat')


def part2(s: Optimize):
    s.push()
    s.add(rcounts['ORE'] == 1000000000000)
    s.maximize(rcounts['FUEL'])
    s.check()

    if m := s.model():
        s.pop()
        return m.evaluate(produced['FUEL'])

    raise ValueError('Part 2 unsat')


a1 = part1(s)
print('part1:', a1)

a2 = part2(s)
print('part2:', a2)

assert a1 == 720484
assert a2 == 1993284
