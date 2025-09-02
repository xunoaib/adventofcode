#!/usr/bin/env python3
import json
import math
import re
import sys
from dataclasses import asdict, dataclass, field
from functools import cache
from heapq import heappop, heappush
from pathlib import Path

ORE, CLAY, OBSIDIAN, GEODE = range(4)


@dataclass(frozen=True, order=True)
class Resources:
    '''Represents any collection of resources'''
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

    def exceeds_any(self, threshold: 'Resources'):
        '''Determines if the current resources exceeds any corresponding resources in the threshold'''
        return any(s > t for s, t in zip(self, threshold))

    def __getitem__(self, index: int):
        values = (self.ore, self.clay, self.obsidian, self.geode)
        return values[index]

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

    def __getitem__(self, index: int):
        values = (self.ore, self.clay, self.obsidian, self.geode)
        return values[index]

    def add(self, robot_type: int):
        assert robot_type in range(4)
        return Bots(
            ore=self.ore + (robot_type == ORE),
            clay=self.clay + (robot_type == CLAY),
            obsidian=self.obsidian + (robot_type == OBSIDIAN),
            geode=self.geode + (robot_type == GEODE),
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


def max_resource_cost(blueprint: Blueprint):
    '''Calculate the maximum cost of a blueprint's resources'''

    geode = clay = obsidian = ore = 0
    for costs in blueprint:
        ore = max(ore, costs.ore)
        clay = max(clay, costs.clay)
        obsidian = max(obsidian, costs.obsidian)
        geodes = max(geode, costs.geode)

    return Resources(geode=geode, obsidian=obsidian, clay=clay, ore=ore)


def maximize_geodes(
    blueprint: Blueprint,
    bots: Bots,
    resources: Resources,
    minutes_left: int,
):
    q = [(resources, bots, minutes_left)]
    visited = {q[0]}
    best_geodes = 0
    i = 0

    # Identify max costs to avoid building more robots than needed
    max_costs = max_resource_cost(blueprint)

    while q:
        resources, bots, minleft = heappop(q)

        i += 1
        if i % 200000 == 0:
            print(
                f'BP {blueprint.id}:',
                str(len(q)).rjust(8),
                str(len(visited)).rjust(8),
                minleft,
                str(resources).ljust(49),
                str(bots).ljust(49),
            )

        if minleft == 0:
            if resources.geode > best_geodes:
                best_geodes = resources.geode
                print(f'\033[92m>>>>> NEW BEST: {best_geodes} <<<<<\033[0m')
            continue

        # Collect resources from bots
        gathered = bots.gather()

        # Greedily build a geode robot (NOTE: could be wrong)
        if resources.can_build(blueprint.geode):
            item = (
                resources.subtract(blueprint.geode).add(gathered),
                bots.add(GEODE),
                minleft - 1,
            )
            if item not in visited:
                visited.add(item)
                heappush(q, item)
            continue

        # Try to build each type of robot
        for robot_type, cost in enumerate(list(blueprint)[:-1]):
            # Avoid building more robots than the max resource consumption rate
            if bots[robot_type] >= max_costs[robot_type]:
                continue

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

    return best_geodes


def simulate(blueprints: list[Blueprint], minutes_left: int):
    bots = Bots(ore=1)
    resources = Resources()

    cache = Path(f'results_{minutes_left}min.json')
    results = json.load(open(cache)) if cache.exists() else {}

    for idx, blueprint in enumerate(blueprints):
        print(f'\n>> Blueprint {blueprint.id}\n')

        if blueprint.id not in results:
            results[
                blueprint.id
            ] = maximize_geodes(blueprint, bots, resources, minutes_left)

            with open(cache, 'w') as f:
                json.dump(results, f)

        print(
            f'\033[95mBlueprint #{blueprint.id} best: {results[blueprint.id]} geodes\033[0m'
        )

    return results


def main():
    lines = sys.stdin.read().strip().splitlines()

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

    a1_results = simulate(blueprints, 24)
    ans1 = sum(i * n for i, n in a1_results.items())
    print('part1:', ans1)

    a2_results = simulate(blueprints[:3], 32)
    ans2 = math.prod(a2_results.values())
    print('part2:', ans2)

    assert ans1 == 2193
    assert ans2 == 7200


if __name__ == '__main__':
    main()
