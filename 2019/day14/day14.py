import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from z3 import Int, Solver


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
    recipe = Recipe(inputs, output)
    recipe_lookup[output.name] = recipe
    recipes.append(recipe)

# Allow creating one ORE at any time
recipe = Recipe([], Resource('ORE', 1))
recipe_lookup['ORE'] = recipe
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


# Create variables representing the total amount of each resource
z_res = {r.output.name: Int(f'{r.output.name}') for r in recipes}

# Create variables representing the number of times each reaction occurs
rcounts = {r.output.name: Int(f'rcount_{r.output.name}') for r in recipes}

zreactions = [ZReaction(r.output.name) for r in recipes]

# Express outputs based on reaction count and inputs
zr = zreactions[0]
print(zr.input_zvar_counts)
print(zr.output_zvar_count)
print(zr.input_zvar_counts_dict)

# Represent total counts of each resource (ie: produced - consumed)
net_res: dict[str, Any] = {name: 0 for name in z_res}
for zreaction in zreactions:

    # Add outputs
    net_res[zreaction.reaction.output.name] += zreaction.output_zvar_count

    # Subtract inputs
    for name, expr in zreaction.input_zvar_counts_dict.items():
        net_res[name] -= expr

for k, v in net_res.items():
    print('>>>', k)
    print(v)
    print()
