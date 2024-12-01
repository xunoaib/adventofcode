#!/usr/bin/env python3
import copy
import re
import numpy as np
import sys
from collections import Counter, defaultdict
from itertools import permutations, product, pairwise
from heapq import heappop, heappush

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff and coff):
            yield r + roff, c + coff


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


def main():
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


if __name__ == '__main__':
    main()
