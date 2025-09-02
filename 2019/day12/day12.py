#!/usr/bin/env python3
import re
import sys
from itertools import combinations


def apply_gravity(moons):
    netvelocity = [[0, 0, 0] for _ in range(len(moons))]
    for m1, m2 in combinations(range(moons), 2):
        p1 = moons[m1]
        p2 = moons[m2]
        for axis in [0, 1, 2]:
            if p1[axis] > p2[axis]:
                d1, d2 = 1, -1
            elif p1[axis] < p2[axis]:
                d1, d2 = -1, 1
            else:
                d1 = d2 = 0
            netvelocity[m1][axis] += d1
            netvelocity[m2][axis] -= d2
    return netvelocity


moons = [
    list(map(int, m))
    for m in re.findall(r'<x=(.*), y=(.*), z=(.*)>', sys.stdin.read())
]

velocities = {i: [0, 0, 0] for i in range(len(moons))}

for _ in range(1000):
    apply_gravity(moons)
    exit(0)
