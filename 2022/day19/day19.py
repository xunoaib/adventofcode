#!/usr/bin/env python3
import re
import sys
from dataclasses import asdict, dataclass
from functools import cache


@dataclass(frozen=True)
class Cost:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


@dataclass(frozen=True)
class Blueprint:
    id: int
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost


@dataclass(frozen=True)
class Bots:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


@dataclass(frozen=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


@cache
def can_build(resources, cost_tuple):
    return all(res >= cost for res, cost in zip(resources, cost_tuple))


def subtract(tup1, tup2):
    return tuple(x - y for x, y in zip(tup1, tup2))


def add(tup1, tup2):
    return tuple(x + y for x, y in zip(tup1, tup2))


best = (0, 0, 0, 0)
histories = {}


def reset():
    global best, histories
    best = (0, ) * 4
    histories = {}


@cache
def optimize(blueprint: Blueprint, bots, resources, minute=24):
    global best

    # print(minute, bots, resources)

    if minute <= 0:
        if resources[-1] > best[-1]:
            print(resources)
            best = resources
        return resources

    # if resources[-1] + minute * (bots[-1] + minute) < best[-1]:
    #     return resources

    # first, gather resources
    added_resources = add(resources, bots)

    # permute spending resources on new robots
    results = []
    botcosts = list(enumerate(blueprint))
    for idx, botcost in botcosts[::-1]:
        if can_build(resources, botcost):
            newbots = list(bots)
            newbots[idx] += 1
            newbots = tuple(newbots)
            newresources = subtract(added_resources, botcost)
            newcount = optimize(blueprint, newbots, newresources, minute - 1)
            results.append(newcount)
    results.append(optimize(blueprint, bots, added_resources, minute - 1))

    return max(results, key=lambda tup: tup[-1])


def main():
    with open('sample.in') as f:
        lines = f.read().strip().splitlines()

    blueprints = []
    for i, line in enumerate(lines):
        c = list(map(int, re.findall(r'\d+', line)))
        blueprints.append(
            Blueprint(
                id=c[0],
                ore=Cost(ore=c[1]),
                clay=Cost(ore=c[2]),
                obsidian=Cost(ore=c[3], clay=c[4]),
                geode=Cost(ore=c[5], obsidian=c[6]),
            )
        )

    bots = Bots(ore=1)
    resources = Resources()

    for idx, blueprint in enumerate(blueprints):
        reset()
        result = optimize(blueprint, bots, resources)
        print('Blueprint', idx + 1, 'max =', result[-1], result)

    # ans1 = part1(lines)
    # print('part1:', ans1)

    # ans2 = part2(lines)
    # print('part2:', ans2)

    # assert ans1 == 0
    # assert ans2 == 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('interrupted')
