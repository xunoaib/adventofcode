#!/usr/bin/env python3

import sys
from itertools import product

dirs = [(r,c) for r,c in product([-1,0,1], [-1,0,1]) if r or c]

def count(r, c):
    total = 0
    for roff, coff in dirs:
        R, C = r, c
        for ch in 'XMAS':
            if d.get((R,C)) != ch:
                break
            R += roff
            C += coff
        else:
            total += 1
    return total

g = []
for line in sys.stdin:
    line = line.strip()
    g.append(line)

d = {}
for r, row in enumerate(g):
    for c, ch in enumerate(row):
        d[r,c] = ch

p1 = 0
for (r,c), ch in d.items():
    if ch == 'X':
        p1 += count(r,c)

print('part1:', p1)

p2 = 0
for (r,c), ch in d.items():
    if ch == 'A':

        op1 = sorted([
            d.get((r-1, c-1), ''),
            d.get((r+1, c+1), '')
        ])

        op2 = sorted([
            d.get((r+1, c-1), ''),
            d.get((r-1, c+1), '')
        ])

        if op1 == op2 == list('MS'):
            p2 += 1

print('part2:', p2)
