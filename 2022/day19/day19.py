#!/usr/bin/env python3
import re
import sys
from dataclasses import asdict, dataclass, field
from functools import cache
from heapq import heappop, heappush


@dataclass(frozen=True, order=True)
class Resources:
    '''How many of each resource we have'''
    sort_index: tuple = field(init=False, repr=False)

    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0

    def __post_init__(self):
        object.__setattr__(
            self, "sort_index",
            (-self.geode, -self.obsidian, -self.clay, -self.ore)
        )

    def __iter__(self):
        return iter((self.ore, self.clay, self.obsidian, self.geode))

    # def __getitem__(self, index: int):
    #     values = (self.ore, self.clay, self.obsidian, self.geode)
    #     return values[index]

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
    sort_index: tuple = field(init=False, repr=False)

    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0

    def __iter__(self):
        return iter((self.ore, self.clay, self.obsidian, self.geode))

    def __post_init__(self):
        object.__setattr__(
            self, "sort_index",
            (-self.geode, -self.obsidian, -self.clay, -self.ore)
        )

    # def __getitem__(self, index: int):
    #     values = (self.ore, self.clay, self.obsidian, self.geode)
    #     return values[index]

    def add(self, robot_type: int):
        assert robot_type in range(4)
        return Bots(
            ore=self.ore + (robot_type == 0),
            clay=self.clay + (robot_type == 1),
            obsidian=self.obsidian + (robot_type == 2),
            geode=self.geode + (robot_type == 3),
        )

    def gather(self):
        '''Gathers resources, returning the amount gathered'''
        return Resources(
            ore=self.ore,
            clay=self.clay,
            obsidian=self.obsidian,
            geode=self.geode,
        )


@dataclass(frozen=True)
class Blueprint:
    '''Resource costs for each type of robot'''
    id: int
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources

    def __iter__(self):
        return iter((self.ore, self.clay, self.obsidian, self.geode))

    # def __getitem__(self, index: int):
    #     values = (self.ore, self.clay, self.obsidian, self.geode)
    #     return values[index]


def maximize_geodes(
    blueprint: Blueprint,
    bots: Bots,
    resources: Resources,
    minutes_left: int,
):
    q = [(resources, bots, minutes_left)]
    visited = {q[0]}

    best_geodes = 0

    while q:
        resources, bots, minleft = heappop(q)

        if minleft == 0:
            if resources.geode > best_geodes:
                best_geodes = resources.geode
                print(best_geodes)
            continue

        # Collect resources from bots
        gathered = bots.gather()

        # Try to build each type of robot
        for robot_type, cost in enumerate(blueprint):
            if resources.can_build(cost):
                item = (
                    resources.subtract(cost).add(gathered),
                    bots.add(robot_type),
                    minleft - 1,
                )
                if item not in visited:
                    visited.add(item)
                    heappush(q, item)

        item = (resources.add(gathered), bots, minleft - 1)
        if item not in visited:
            visited.add(item)
            heappush(q, item)


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


if __name__ == '__main__':
    main()
