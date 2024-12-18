#!/usr/bin/env python3

import sys


def neighbors4(r, c):
    for roff, coff in (-1, 0), (0, 1), (1, 0), (0, -1):
        if not (roff and coff):
            yield r + roff, c + coff

def shortest(bites):
    bites = set(bites)
    q = [(0, (0,0))]
    seen = {(0,0)}

    while q:
        step, pos = q.pop(0)
        if pos == (WIDTH-1, HEIGHT-1):
            return step

        for r,c in neighbors4(*pos):
            if all([
                r in range(HEIGHT),
                c in range(WIDTH),
                (r,c) not in bites,
                (r,c) not in seen
            ]):
                q.append((step + 1, (r,c)))
                seen.add((r,c))

WIDTH = HEIGHT = 71

lines = sys.stdin.read().strip().split('\n')
bites = [tuple(map(int, line.split(',')))[::-1] for line in lines]

def part2():
    for i in range(len(bites)):
        if not shortest(bites[:i+1]):
            r,c = bites[i]
            return f'{c},{r}'

a1 = shortest(bites[:1024])
print('part1:', a1)

a2 = part2()
print('part2:', a2)

assert a1 == 382
assert a2 == '6,36'
