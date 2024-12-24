#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

from z3 import Bool, Solver, sat

# @dataclass
# class Gate:
#     gtype: str
#     left: 'Gate | '
#     right: 'Gate | '


a,b = sys.stdin.read().strip().split('\n\n')

a = a.split('\n')
b = b.split('\n')

def part1():
    s = Solver()

    wires = {}

    for v in a:
        x,y = v.split(': ')
        wires[x] = vout = Bool(f'{v}')
        s.add(vout == bool(int(y)))

    for line in b:
        vin1, op, vin2, _, vout = line.split()
        if vin1 not in wires:
            wires[vin1] = Bool(f'{vin1}')
        if vin2 not in wires:
            wires[vin2] = Bool(f'{vin2}')
        if vout not in wires:
            wires[vout] = Bool(f'{vout}')

        zin1 = wires[vin1]
        zin2 = wires[vin2]
        zout = wires[vout]

        match op:
            case 'XOR':
                s.add(zin1 ^ zin2 == zout)
            case 'OR':
                s.add(zin1 | zin2 == zout)
            case 'AND':
                s.add(zin1 & zin2 == zout)

    if s.check() == sat:
        m = s.model()
        zs = [z for w,z in sorted(wires.items()) if w.startswith('z')]
        vals  = [bool(m[z]) for z in zs][::-1]
        return int(''.join(['1' if v else '0' for v in vals]), 2)

a1 = part1()
print('part1:', a1)
