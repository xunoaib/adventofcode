import copy
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from itertools import batched, combinations, pairwise
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


@dataclass
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


def main():
    groups = batched(map(int, re.findall(r'-?\d+', sys.stdin.read())), 3)
    moons = [Moon(position=Vec(*arg), velocity=Vec(0, 0, 0)) for arg in groups]
    system = System(moons)

    state_times: list[dict[tuple[int, ...], list[int]]
                      ] = [defaultdict(list[int]) for _ in 'xyz']
    xhist, yhist, zhist = state_times

    step = 0

    # Log initial state
    for m in moons:
        for hist in state_times:
            hist[system.axis_coords(X)].append(step)

    ans1 = ans2 = 0

    print(system)

    while True:
        step += 1
        dvs = calculate_velocity_deltas(moons)
        system = system.step()
        print(system)
        exit(0)

        if step == 1000:
            ans1 = calculate_energy(moons, velocities)
            print('part1:', ans1)

        new_x = extract_dim(moons, X)
        new_y = extract_dim(moons, Y)
        new_z = extract_dim(moons, Z)

        x_hist[new_x].append(step)
        y_hist[new_y].append(step)
        z_hist[new_z].append(step)

        # for d in (x_hist, y_hist, z_hist):
        #     if len(d[new_x]) > 2:
        #         print(pwdiff(d[new_x]))

        if step > 1000000:
            break

    import pickle

    pickle.dump((x_hist, y_hist, z_hist), open('histories.pkl', 'wb'))

    assert ans1 == 9493, ans1


if __name__ == '__main__':
    main()
