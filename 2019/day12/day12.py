#!/usr/bin/env python3
import copy
import re
import sys
from itertools import batched, combinations


def apply_gravity(moons: list, velocities: list):
    velocities = copy.deepcopy(velocities)
    delta_velocities = [[0, 0, 0] for _ in velocities]
    for m1, m2 in combinations(range(len(moons)), 2):
        p1 = moons[m1]
        p2 = moons[m2]
        for axis in [0, 1, 2]:
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

for i in range(1000):
    moons, velocities = apply_gravity(moons, velocities)

ans1 = calculate_energy(moons, velocities)
print('part1:', ans1)

assert ans1 == 9493
