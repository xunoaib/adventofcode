import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from z3 import Int, Optimize, Solver


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
    def input_zvars(self):
        return [z_res[inp.name] for inp in self.reaction.inputs]

    @property
    def input_zvar_counts(self):
        return [
            z_res[inp.name] * inp.amount * rcounts[self.name]
            for inp in self.reaction.inputs
        ]

    @property
    def input_zvar_counts_dict(self):
        return {
            inp.name: z_res[inp.name] * inp.amount * rcounts[self.name]
            for inp in self.reaction.inputs
        }

    @property
    def output_zvar(self):
        return z_res[self.name]

    @property
    def output_zvar_count(self):
        return z_res[self.name
                     ] * self.reaction.output.amount * rcounts[self.name]

    @property
    def reaction_count_zvar(self):
        return rcounts[self.name]


s = Optimize()

# Create variables representing the total amount of each resource
z_res = {r.output.name: Int(f'{r.output.name}') for r in recipes}

# Create variables representing the number of times each reaction occurs
rcounts = {r.output.name: Int(f'rcount_{r.output.name}') for r in recipes}

zreactions = [ZReaction(r.output.name) for r in recipes]

# Ensure counts are positive
for zvar in rcounts.values():
    s.add(zvar >= 0)

# Represent total counts of each resource (ie: produced - consumed)
produced = {n: 0 for n in z_res}
consumed = {n: 0 for n in z_res}
# net_res: dict[str, Any] = {name: 0 for name in z_res}

for zreaction in zreactions:
    # Add outputs
    produced[zreaction.reaction.output.name] += zreaction.output_zvar_count

    # Subtract inputs
    for name, expr in zreaction.input_zvar_counts_dict.items():
        consumed[name] += expr

# Ensure resource consumption never exceeds production
totals = {}
for name in {*produced, *consumed}:
    totals[name] = total = produced.get(name, 0) - consumed.get(name, 0)
    s.add(total >= 0)

# Specify goal condition
s.add(z_res['FUEL'] == 1)

assert s.check()

# print('Minimizing')
# s.minimize(rcounts['ORE'])
# print('Minimized:', res)

if m := s.model():
    print(m[z_res['ORE']])
    print(m.evaluate(produced['ORE']))
    print(m.evaluate(rcounts['ORE']))
else:
    print('unsat')
