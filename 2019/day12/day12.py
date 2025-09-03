import copy
import math
import pickle
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from hashlib import md5
from itertools import batched, combinations, pairwise
from pathlib import Path
from typing import Literal

X, Y, Z = range(3)


@dataclass(frozen=True)
class Vec:
    x: int
    y: int
    z: int

    def __add__(self, other: 'Vec'):
        return Vec(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __getitem__(self, index: int):
        return (self.x, self.y, self.z)[index]

    def __str__(self):
        return f'<x={self.x:2}, y={self.y:3}, z={self.z:2}>'

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


@dataclass(frozen=True)
class Moon:
    position: Vec
    velocity: Vec

    def __str__(self):
        return f'pos={self.position}, vel={self.velocity}'

    def energy(self):
        return abs(sum(map(abs, self.position)) * sum(map(abs, self.velocity)))


@dataclass(frozen=True)
class System:
    moons: list[Moon]
    time: int = 0

    @property
    def x_coords(self):
        return tuple(moon.position.x for moon in self.moons)

    @property
    def y_coords(self):
        return tuple(moon.position.y for moon in self.moons)

    @property
    def z_coords(self):
        return tuple(moon.position.z for moon in self.moons)

    def axis_coords(self, axis: int):
        match axis:
            case 0:
                return self.x_coords
            case 1:
                return self.y_coords
            case 2:
                return self.z_coords
            case _:
                raise IndexError()

    def __str__(self):
        return f'After {self.time} steps:\n' + '\n'.join(
            f'{moon}' for moon in self.moons
        ) + '\n'

    def step(self):
        dvs = calculate_velocity_deltas(self.moons)
        moons = [
            Moon(
                position=m.velocity + dv + m.position,
                velocity=m.velocity + dv,
            ) for m, dv in zip(self.moons, dvs)
        ]
        return System(moons, self.time + 1)

    def energy(self):
        return sum(m.energy() for m in self.moons)


def pairwise_diff(nums):
    return [b - a for a, b in pairwise(nums)]


def calculate_velocity_deltas(moons: list[Moon]):
    '''Calculates the velocity deltas for each moon.'''

    delta_velocities = [Vec(0, 0, 0) for _ in moons]
    for m1, m2 in combinations(range(len(moons)), 2):
        pos1 = moons[m1].position
        pos2 = moons[m2].position

        dv1, dv2 = [], []
        for axis in [X, Y, Z]:
            if pos1[axis] > pos2[axis]:
                d1, d2 = -1, 1
            elif pos1[axis] < pos2[axis]:
                d1, d2 = 1, -1
            else:
                d1 = d2 = 0
            dv1.append(d1)
            dv2.append(d2)

        delta_velocities[m1] += Vec(*dv1)
        delta_velocities[m2] += Vec(*dv2)

    return delta_velocities


def part1(system: System):
    for _ in range(1000):
        system = system.step()
    return system.energy()


def part2(system: System, cache_id: str):
    histories: list[dict[tuple[int, ...],
                         list[int]]] = [defaultdict(list[int]) for _ in 'xyz']
    xhist, yhist, zhist = histories

    # Log initial state
    initial_states = xinit, yinit, zinit = [
        system.axis_coords(axis) for axis in [X, Y, Z]
    ]
    for axis, hist in enumerate(histories):
        hist[system.axis_coords(axis)].append(0)

    ans2 = step = 0

    while True:
        system = system.step()
        step += 1

        # Log positions
        for axis, hist in enumerate(histories):
            hist[system.axis_coords(axis)].append(step)

        # Wait until we find a repeating pattern on each axis
        if all(
            len(hist[init]) >= 5
            for hist, init in zip(histories, initial_states)
        ):
            break

    # Repeating states seems to occur at two alternating intervals.
    # We want a single interval, so we merge the two alternating ones.
    # Note: This might be input/puzzle-specific.

    xdiffs = pairwise_diff(xhist[xinit])
    ydiffs = pairwise_diff(yhist[yinit])
    zdiffs = pairwise_diff(zhist[zinit])

    intervals = []
    for diffs in (xdiffs, ydiffs, zdiffs):
        assert len(set(diffs[::2])) == len(set(diffs[1::2])) == 1
        intervals.append(diffs[0] + diffs[1])

    # print('X:', xdiffs)
    # print('Y:', ydiffs)
    # print('Z:', zdiffs)

    return math.lcm(*intervals)


def main():
    data = sys.stdin.read()
    groups = batched(map(int, re.findall(r'-?\d+', data)), 3)
    moons = [Moon(position=Vec(*arg), velocity=Vec(0, 0, 0)) for arg in groups]
    system = System(moons)

    ans1 = part1(system)
    print('part1:', ans1)

    ans2 = part2(system, md5(data.encode()).hexdigest())
    print('part2:', ans2)

    assert ans1 == 9493
    assert ans2 == 326365108375488


if __name__ == '__main__':
    main()
