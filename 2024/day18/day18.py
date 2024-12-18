#!/usr/bin/env python3

import sys
from heapq import heappop, heappush
from time import time

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff

def shortest(corrupted):
    start = (0,0)
    goal = (WIDTH-1, HEIGHT-1)

    q = [(0, start)]
    seen = {start}
    while q:
        step, pos = heappop(q)
        if pos == goal:
            return step

        for r,c in neighbors4(*pos):
            if all([
                r in range(HEIGHT),
                c in range(WIDTH),
                (r,c) not in corrupted,
                (r,c) not in seen
            ]):
                heappush(q, (step + 1, (r,c)))
                seen.add((r,c))

WIDTH = HEIGHT = 71

lines = sys.stdin.read().strip().split('\n')
all_bites = [tuple(map(int, line.split(',')))[::-1] for line in lines]

def part1():
    bites = set(all_bites[:1024])
    return shortest(bites)

def part2():
    last = time()
    for i in range(len(all_bites)):
        bites = set(all_bites[:i])
        if not shortest(bites):
            r,c = all_bites[i-1]
            return f'{c},{r}'

        if time() - last > 1:
            print('checked step', i)
            last = time()

a1 = part1()
print('part1:', a1)

a2 = part2()
print('part2:', a2)

assert a1 == 382
assert a2 == '6,36'
