#!/usr/bin/env python
import sys
import parse
from pprint import pprint
from collections import defaultdict

# spaghetti alert - proceed with caution

class Food:
    def __init__(self, line, name):
        ingredients, allergens = parse.parse('{} (contains {})', line)
        self.ingredients = ingredients.split()
        self.allergens = allergens.split(', ')
        self.name = name

    def __repr__(self):
        return f'F{self.name}'

class Allergen:
    def __init__(self, name):
        self.name = name
        self.ingredients = set()
        self.ingredient = None

    def __repr__(self):
        return f'{self.name}'

class Ingredient:
    def __init__(self, name):
        self.name = name
        self.allergens = set()

    def __repr__(self):
        return f'{self.name}'

def find_allergens(foods):
    '''Find ingredients that always appear with the same allergens'''
    candidates = {}
    for food in foods:
        for alg in food.allergens:
            if alg not in candidates:
                candidates[alg] = set(food.ingredients)
            else:
                candidates[alg] &= set(food.ingredients)
    return candidates

def assign_allergens(ingredients, depth=0):
    if depth >= len(ingredients):
        return True

    # only consider unused rules for this column
    ingredient = ingredients[depth]
    for allergen in ingredient.allergens:
        if allergen.ingredient:
            continue
        allergen.ingredient = ingredient
        if assign_allergens(ingredients, depth+1):
            return True
        allergen.ingredient = None
    return False

foods = [Food(line,i) for i,line in enumerate(sys.stdin)]

# map allergens to possible ingredients
candidates = find_allergens(foods)
pprint(candidates)

# gather all ingredients
ingredients = set()
allergens = set()
for food in foods:
    ingredients |= set(food.ingredients)
    allergens |= set(food.allergens)

# gather all candidate ingredients for allergens
algcands = set()
for allergen, ings in candidates.items():
    algcands |= ings

safe = ingredients - algcands

# count the number of foods with safe ingredients
count = 0
for food in foods:
    matches = safe & set(food.ingredients)
    count += len(matches)
print('part1:', count)

# part 2
allergens = {name: Allergen(name) for name in allergens}
ingredients = {name: Ingredient(name) for name in ingredients - safe}

# find which allergens can correspond to each ingredient
algcands = defaultdict(set)
for allergen, inglist in candidates.items():
    algobj = allergens[allergen]
    for ing in inglist:
        algcands[ing].add(allergen)
        ingobj = ingredients[ing]

        # link ingredients and allergens
        ingobj.allergens.add(algobj)
        algobj.ingredients.add(ingobj)

# sort by number of allergy candidates to reduce failed paths
sorted_ings = sorted(ingredients.values(), key=lambda ing: len(ing.allergens))
assign_allergens(sorted_ings)

dangerous = []
for allergen in allergens.values():
    dangerous.append(allergen)

groups = ((a, a.ingredient) for a in allergens.values())
dangerous = sorted(groups, key=lambda group: group[0].name)

answer = ','.join(ing.name for alg,ing in dangerous)
print('part2:', answer)
