#!/usr/bin/env python3
import re
import sys
from dataclasses import asdict, dataclass
from functools import cache
from heapq import heappop, heappush


@dataclass(frozen=True, order=True)
class Resources:
    '''How many of each resource we have'''
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __iter__(self):
        yield self.ore
        yield self.clay
        yield self.obsidian
        yield self.geode

    def can_build(self, cost: 'Resources'):
        return all(
            [
                self.geode >= cost.geode,
                self.clay >= cost.clay,
                self.obsidian >= cost.obsidian,
                self.ore >= cost.ore,
            ]
        )

    def subtract(self, cost: 'Resources'):
        return Resources(
            geode=self.geode - cost.geode,
            clay=self.clay - cost.clay,
            obsidian=self.obsidian - cost.obsidian,
            ore=self.ore - cost.ore,
        )

    def add(self, add: 'Resources'):
        return Resources(
            geode=self.geode + add.geode,
            clay=self.clay + add.clay,
            obsidian=self.obsidian + add.obsidian,
            ore=self.ore + add.ore,
        )


@dataclass(frozen=True, order=True)
class Bots:
    '''How many of each bot we have'''
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __iter__(self):
        yield self.ore
        yield self.clay
        yield self.obsidian
        yield self.geode


@dataclass(frozen=True)
class Blueprint:
    '''Resource costs for each type of robot'''
    id: int
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources

    def __iter__(self):
        yield self.ore
        yield self.clay
        yield self.obsidian
        yield self.geode


def old_optimize(
    blueprint: Blueprint,
    bots: Bots,
    resources: Resources,
    minutes_left: int,
):
    if minutes_left <= 0:
        if resources.geode > best_geode_count:
            print(resources)
            best_geode_count = resources.geode
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
            newcount = maximize_geodes(
                blueprint, newbots, newresources, minutes_left - 1
            )
            results.append(newcount)
    results.append(
        maximize_geodes(blueprint, bots, added_resources, minutes_left - 1)
    )

    return max(results, key=lambda tup: tup[-1])


def maximize_geodes(
    blueprint: Blueprint,
    bots: Bots,
    resources: Resources,
    minutes_left: int,
):
    q = [(resources, bots, minutes_left)]
    visited = {q[0]}

    while q:
        resources, bots, minleft = heappop(q)

        # Try to build each type of robot
        for res, botcost in zip(resources, blueprint):
            print(res, botcost)


def main():
    with open('sample.in') as f:
        lines = f.read().strip().splitlines()

    blueprints: list[Blueprint] = []
    for i, line in enumerate(lines):
        c = list(map(int, re.findall(r'\d+', line)))
        blueprints.append(
            Blueprint(
                id=c[0],
                ore=Resources(ore=c[1]),
                clay=Resources(ore=c[2]),
                obsidian=Resources(ore=c[3], clay=c[4]),
                geode=Resources(ore=c[5], obsidian=c[6]),
            )
        )

    bots = Bots(ore=1)
    resources = Resources()
    minutes_left = 24

    for idx, blueprint in enumerate(blueprints):
        print(f'\n>> Blueprint {blueprint.id}\n')
        maximize_geodes(blueprint, bots, resources, minutes_left)

        # reset()
        # result = maximize_geodes(blueprint, bots, resources, minutes=24)
        # print(f'Blueprint {blueprint.id}: max = {result}')

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
