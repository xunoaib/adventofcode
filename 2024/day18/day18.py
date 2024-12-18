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

def print_state(corrupted, path=tuple()):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if (r,c) in path:
                ch = 'O'
            else:
                ch = '#' if (r,c) in corrupted else '.'
            print(ch, end='')
        print()
    print()

def shortest(corrupted):
    start = (0,0)
    goal = (WIDTH-1, HEIGHT-1)

    q = [(0, start)]
    seen = {start}
    parents = {}
    while q:
        step, pos = heappop(q)
        if pos == goal:

            path = {pos}
            while pos := parents.get(pos):
                path.add(pos)

            print_state(corrupted, path)
            return step

        # if step not in history:
        #     print('stepping new:', step)
        #     history[step] = simulate(*history[step-1])

        for r,c in neighbors4(*pos):
            if all([
                r in range(HEIGHT),
                c in range(WIDTH),
                # (r,c) not in history[step],
                (r,c) not in corrupted,
                (r,c) not in seen
            ]):
                heappush(q, (step + 1, (r,c)))
                seen.add((r,c))
                parents[r,c] = pos

def simulate(bites, corrupted):
    bites = {(r+1,c) for r,c in bites if r < HEIGHT}
    return bites, corrupted | bites

lines = sys.stdin.read().strip().split('\n')

SAMPLE = False

if SAMPLE:
    lines = lines[:12] # sample
    WIDTH = HEIGHT = 7
else:
    lines = lines[:1024] # part 1
    WIDTH = HEIGHT = 71

bites = set()
for line in lines:
    c,r = map(int, line.split(','))
    bites.add((r,c))

# 138 not right
# 140


corrupted = bites.copy()

# # sample
# # bites, corrupted = simulate(bites, corrupted)
# print_state(corrupted)
# print('sample:', shortest(corrupted))
# exit(0)

# print_state(corrupted)
# exit(0)

# for step in range(1024):
#     bites, corrupted = simulate(bites, corrupted)

print_state(corrupted)

print('part1:', shortest(corrupted))
exit(0)

# history = {0: (bites, corrupted)}
history = {}
step = 0

# for step in range(1024):
#     history[step+1] = bites, corrupted = simulate(bites, corrupted)

bites, corrupted = simulate(bites, corrupted)

print_state(corrupted)
a1 = shortest(corrupted)

# a1 = shortest(history[1024])
print('part1:', a1)

a1 = a2 = 0

# print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
