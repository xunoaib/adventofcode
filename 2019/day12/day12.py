#!/usr/bin/env python3
import copy
import re
import sys
from collections import defaultdict
from itertools import batched, combinations, pairwise
from typing import Literal

X, Y, Z = range(3)


def extract_dim(moons: tuple, dim: int):
    return tuple(m[dim] for m in moons)


def pwdiff(nums):
    return [b - a for a, b in pairwise(nums)]


def apply_gravity(moons: list, velocities: list):
    velocities = copy.deepcopy(velocities)
    delta_velocities = [[0, 0, 0] for _ in velocities]
    for m1, m2 in combinations(range(len(moons)), 2):
        p1 = moons[m1]
        p2 = moons[m2]
        for axis in [X, Y, Z]:
            if p1[axis] > p2[axis]:
                d1, d2 = -1, 1
            elif p1[axis] < p2[axis]:
                d1, d2 = 1, -1
            else:
                d1 = d2 = 0
            delta_velocities[m1][axis] += d1
            delta_velocities[m2][axis] += d2

    final_velocities = tuple(
        (vx + dvx, vy + dvy, vz + dvz)
        for (vx, vy, vz), (dvx, dvy, dvz) in zip(delta_velocities, velocities)
    )

    # Apply deltas
    return tuple(
        (x + dx, y + dy, z + dz)
        for (x, y, z), (dx, dy, dz) in zip(moons, final_velocities)
    ), final_velocities


def calculate_energy(moons: list, velocities: list):
    return sum(
        abs(sum(map(abs, pos)) * sum(map(abs, vel)))
        for pos, vel in zip(moons, velocities)
    )


def print_status():
    for (x, y, z), (vx, vy, vz) in zip(moons, velocities):
        print(
            f'pos=<x={x:2}, y={y:3}, z={z:2}>, vel=<x={vx:2}, y={vy:2}, z={vz:2}>'
        )


moons = tuple(batched(map(int, re.findall(r'-?\d+', sys.stdin.read())), 3))
velocities = tuple((0, 0, 0) for i in range(len(moons)))

x_hist = defaultdict(list)
y_hist = defaultdict(list)
z_hist = defaultdict(list)

for m in moons:
    x_hist[extract_dim(moons, X)].append(0)
    y_hist[extract_dim(moons, Y)].append(0)
    z_hist[extract_dim(moons, Z)].append(0)

ans1 = ans2 = 0

i = 1
while True:
    moons, velocities = apply_gravity(moons, velocities)

    if i == 1000:
        ans1 = calculate_energy(moons, velocities)
        print('part1:', ans1)

    new_x = extract_dim(moons, X)
    new_y = extract_dim(moons, Y)
    new_z = extract_dim(moons, Z)

    x_hist[new_x].append(i)
    y_hist[new_y].append(i)
    z_hist[new_z].append(i)

    # for d in (x_hist, y_hist, z_hist):
    #     if len(d[new_x]) > 2:
    #         print(pwdiff(d[new_x]))

    i += 1
    if i > 1000000:
        break

import pickle

pickle.dump((x_hist, y_hist, z_hist), open('histories.pkl', 'wb'))

assert ans1 == 9493, ans1
