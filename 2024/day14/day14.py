#!/usr/bin/env python3

import math
import re
import sys
from collections import Counter


def part1(robots):
    robots = step(robots, 100)
    quads = Counter()

    for (r,c),_ in robots:
        mr = h // 2
        mc = w // 2
        if r != h // 2 and c != w // 2:
            quads[r < mr, c < mc] += 1

    return math.prod(quads.values())

def part2(robots):
    for i in range(sys.maxsize):
        s = get_grid(robots)
        if '11111111111111' in s:
            return i
        robots = step(robots)

def step(robots, steps=1):
    res = []
    for p, v in robots:
        npr = (p[0] + v[0] * steps) % h
        npc = (p[1] + v[1] * steps) % w
        res.append(((npr, npc), v))
    return res

def get_grid(robots):
    grid = Counter(p for p,_ in robots)
    out = ''
    for r in range(h):
        for c in range(w):
            out += str(grid.get((r,c), '.'))
        out += '\n'
    return out


robots = []
for line in sys.stdin.read().splitlines():
    m = re.match(r'p=(.*) v=(.*)', line)
    p, v = [tuple(map(int, t.split(',')))[::-1] for t in m.groups()]
    robots.append((p,v))

w,h = 101,103

a1 = part1(robots)
print('part1:', a1)

a2 = part2(robots)
print('part2:', a2)

assert a1 == 216772608
assert a2 == 6888
