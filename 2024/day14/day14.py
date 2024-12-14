#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

import numpy as np


def print_grid(robots):
    grid = Counter()
    for p,v in robots:
        grid[p] += 1
    for r in range(h):
        for c in range(w):
            print(grid.get((r,c), '.'), end='')
        print()
    print()

def add(a,b):
    return (a[0]+b[0]) % h, (a[1]+b[1]) % w

def step(robots, steps=1):
    # res = []
    # for (pr, pc), (vr, vc) in robots:
    #     npr = (pr + vr * 100) % h
    #     npc = (pc + vc * 100) % w
    #     res.append(((npr, npc), (vr, vc)))

    res = []
    for p,v in robots:
        for _ in range(steps):
            p = add(p, v)
        res.append((p,v))
    return res

w,h = 101,103
# w,h = 11,7

robots = []

for line in sys.stdin.read().splitlines():
    m = re.match(r'p=(.*) v=(.*)', line)
    (pc, pr), (vc, vr) = [tuple(map(int, t.split(','))) for t in m.groups()]
    p = (pr, pc)
    v = (vr, vc)
    robots.append((p,v))

__import__('pprint').pprint(robots)

# robots = [((4,2), (-3,2))]
# print_grid(robots)
# for i in range(5):
#     print(i+1)
#     robots = step(robots)
#     print_grid(robots)
# exit(0)
# print_grid(robots)

robots = step(robots, 100)

print_grid(robots)

# # count quads
quads = Counter()
for (r,c),v in robots:
    mr = h // 2
    mc = w // 2
    if r == h // 2 or c == w // 2:
        continue
    quads[(r < mr, c < mc)] += 1

__import__('pprint').pprint(quads)

grid = Counter()
for p,v in robots:
    grid[p] += 1
for r in range(h):
    for c in range(w):
        if r == h // 2 or c == w // 2:
            print('X', end='')
        else:
            print(grid.get((r,c), '.'), end='')
    print()
print()

a1 = 1
for c in quads.values():
    a1 *= c

print('part1:', a1)
# print('part2:', a2)

# 7464683520
# 83017935

# assert a1 == 0
# assert a2 == 0
