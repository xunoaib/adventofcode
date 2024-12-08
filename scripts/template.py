#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

import numpy as np

for line in sys.stdin.read().splitlines():
    print(line)


DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff and coff):
            yield r + roff, c + coff

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

for line in lines:
    print(line)

a1 = a2 = 0

# print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
