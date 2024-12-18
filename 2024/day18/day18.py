#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff and coff):
            yield r + roff, c + coff

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff

def print_state(state, height=7, width=7):
    for r in range(height):
        for c in range(width):
            ch = '#' if (r,c) in state else '.'
            print(ch, end='')
        print()
    print()

# WIDTH = HEIGHT = 70
WIDTH = HEIGHT = 7

def shortest(start_step, start=(0,0), goal=(WIDTH-1, HEIGHT-1)):
    q = [(start_step, start)]
    seen = set()
    while q:
        step, pos = q.pop()
        if pos == goal:
            return step

        if step not in history:
            print('stepping new:', step)
            history[step] = simulate(*history[step-1])

        for r,c in neighbors4(*pos):
            if all([
                   c in range(WIDTH),
                   r in range(HEIGHT),
                   (r,c) not in history[step],
                   (r,c,step+1) not in seen
                   ]):
                heappush(q, (step + 1, (r,c)))
                seen.add((r,c,step))

def simulate(bites, corrupted):
    bites = {(r+1,c) for r,c in bites if r < 70}
    return bites, corrupted | bites

lines = sys.stdin.read().strip().split('\n')

bites = set()
for line in lines[:12]:
    c,r = map(int, line.split(','))
    bites.add((r,c))

corrupted = bites.copy()
history = {0: (bites, corrupted)}

step = 0
for step in range(1024):
    history[step+1] = bites, corrupted = simulate(bites, corrupted)

a1 = shortest(step)
print('part1:', a1)


a1 = a2 = 0

# print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
