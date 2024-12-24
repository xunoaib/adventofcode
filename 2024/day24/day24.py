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

@dataclass
class Gate:
    op: str
    in1: str
    in2: str
    out: str

    def evaluate(self, wires):
        v1 = wires[self.in1]
        v2 = wires[self.in2]

        if isinstance(v1, Gate):
            v1 = v1.evaluate(wires)

        if isinstance(v2, Gate):
            v2 = v2.evaluate(wires)

        match self.op:
            case 'XOR':
                return v1 ^ v2
            case 'OR':
                return v1 | v2
            case 'AND':
                return v1 & v2
        raise NotImplementedError('arst')

def part2():

    def print_trace(name, indent=0):
        var = wires[name]
        if not isinstance(var, Gate):
            print(' '*indent + f'{name} = {var}')
            return var

        print(' '*indent + f'{var}')
        print_trace(var.in1, indent+1)
        print_trace(var.in2, indent+1)

    def trace(name):
        var = wires[name]
        if not isinstance(var, Gate):
            return {name}
        return {name} | trace(var.in1) | trace(var.in1)

    wires = {}

    for v in a:
        name, val = v.split(': ')
        wires[name] = int(val)

    for line in b:
        vin1, op, vin2, _, vout = line.split()
        wires[vout] = gate = Gate(op, vin1, vin2, vout)

    x_vs = [v for w,v in sorted(wires.items()) if w.startswith('x')][::-1]
    x_bstr = ''.join('1' if v else '0' for v in x_vs)
    x_value = int(x_bstr, 2)

    y_vs = [v for w,v in sorted(wires.items()) if w.startswith('y')][::-1]
    y_bstr = ''.join('1' if v else '0' for v in y_vs)
    y_value = int(y_bstr, 2)

    z_value = x_value + y_value  # REAL operation for part 2
    z_value = x_value & y_value  # SAMPLE operation

    z_vs = sorted([w for w in wires if w.startswith('z')])[::-1]
    z_bstr = ''.join('1' if wires[z].evaluate(wires) else '0' for z in z_vs)
    z_calc = int(z_bstr, 2)

    def find_invalid():
        for i, z in enumerate(z_vs[::-1]):
            g = wires[z]
            expected = (z_value >> i) & 1
            print(z, expected, g.evaluate(wires), g)

    print(f'{x_value:>7b}')
    print(f'{y_value:>7b}')
    print('-'*7)
    print(f'{z_value:>7b} expected')
    print(f'{z_calc:>7b} actual')
    print()
    print(f'{x_value} + {y_value} = {z_value} (got {z_calc})')
    print()

    find_invalid()
    exit(0)

    for n, v in sorted(wires.items()):
        if not n.startswith('z'):
            continue
        if n[0] in 'xy':
            continue
        print(n, trace(n))

# a1 = part1()
# print('part1:', a1)

a2 = part2()
print('part2:', a2)
