#!/usr/bin/env python3

import sys
from itertools import product

dirs = [(r,c) for r,c in product([-1,0,1], [-1,0,1]) if r or c]

def count(r_start, c_start):
    total = 0
    for roff, coff in dirs:
        r, c = r_start, c_start
        for ch in 'MAS':
            r += roff
            c += coff
            if d.get((r,c)) != ch:
                break
        else:
            total += 1
    return total

d = {}
for r, row in enumerate(sys.stdin):
    for c, ch in enumerate(row.strip()):
        d[r,c] = ch

p1 = sum(count(r,c) for (r,c), ch in d.items() if ch == 'X')

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
