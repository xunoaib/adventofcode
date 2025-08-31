#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import combinations, pairwise, permutations, product
from typing import Any, Literal

from z3 import Bool, BoolRef, Solver, sat


class LoopError(Exception):
    ...


a, b = sys.stdin.read().strip().split('\n\n')

a = a.split('\n')  # initial wire values
b = b.split('\n')  # gate outputs


def part1():
    s = Solver()

    wires: dict[str, BoolRef] = {}

    for v in a:
        x, y = v.split(': ')
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
        zs = [z for w, z in sorted(wires.items()) if w.startswith('z')]
        vals = [bool(m[z]) for z in zs][::-1]
        return int(''.join(['1' if v else '0' for v in vals]), 2)


@dataclass(order=True)
class EvalableInt(int):
    value: int

    def evaluate(self, wires=None) -> int:
        return int(self)


@dataclass(order=True)
class Gate:
    out: str
    op: str
    in1: str
    in2: str

    def __hash__(self):
        return hash((self.out, self.op, self.in1, self.in2))

    # def __repr__(self):
    #     v1 = wires[self.in1]
    #     v2 = wires[self.in2]
    #     name1 = v1.out if isinstance(v1, Gate) else v1
    #     name2 = v2.out if isinstance(v2, Gate) else v2
    #     # return f'{self.out} <== {name1} {self.op} {name2}'
    #     # return f'Gate({self.out})'
    #     return f'{self.out}'

    def evaluate(self, wires, seen=tuple()) -> int:

        if self in seen:
            raise LoopError()

        seen += (self, )

        v1 = wires[self.in1]
        v2 = wires[self.in2]

        if isinstance(v1, Gate):
            v1 = v1.evaluate(wires, seen)

        if isinstance(v2, Gate):
            v2 = v2.evaluate(wires, seen)

        match self.op:
            case 'XOR':
                return v1 ^ v2
            case 'OR':
                return v1 | v2
            case 'AND':
                return v1 & v2
        raise NotImplementedError('arst')

    @property
    def inputs(self):
        return (self.in1, self.in2)


def part2():
    # global wires

    def print_trace(name, indent=0):
        var = wires[name]
        if not isinstance(var, Gate):
            print(' ' * indent + f'{name} = {var}')
            return var

        print(' ' * indent + f'{var}')
        print_trace(var.in1, indent + 1)
        print_trace(var.in2, indent + 1)

    def trace(name: str):
        var = wires[name]
        if not isinstance(var, Gate):
            return {name}
        return {name} | trace(var.in1) | trace(var.in1)

    wires: dict[str, EvalableInt | Gate] = {}

    for v in a:
        name, val = v.split(': ')
        wires[name] = EvalableInt(int(val))

    for line in b:
        vin1, op, vin2, _, vout = line.split()
        wires[vout] = Gate(vout, op, vin1, vin2)

    x_vs = [v for w, v in sorted(wires.items()) if w.startswith('x')][::-1]
    x_bstr = ''.join('1' if v else '0' for v in x_vs)
    x_value = int(x_bstr, 2)

    y_vs = [v for w, v in sorted(wires.items()) if w.startswith('y')][::-1]
    y_bstr = ''.join('1' if v else '0' for v in y_vs)
    y_value = int(y_bstr, 2)

    # import random
    # x_value = random.randint(1,(1 << len(x_vs))-1)
    # y_value = random.randint(1,(1 << len(y_vs))-1)

    z_expected = x_value + y_value  # REAL operation for part 2
    # z_expected = x_value & y_value  # SAMPLE operation

    z_vs = sorted([w for w in wires if w.startswith('z')])[::-1]
    z_bstr = ''.join('1' if wires[z].evaluate(wires) else '0' for z in z_vs)
    z_actual = int(z_bstr, 2)

    def find_invalid() -> list[list[str]]:
        ''' Find all invalid z bits and the gates/values involved with them '''
        bad = []
        actual_all = []
        expected_all = []
        for i, z in enumerate(z_vs[::-1]):
            g = wires[z]
            actual = g.evaluate(wires)
            expected = (z_expected >> i) & 1
            actual_all.append(actual)
            expected_all.append(expected)
            # color = '\033[92m' if actual == expected else '\033[91m'
            # print(f'{color}{z} {expected} {actual} {g}\033[0m')
            if actual != expected:
                # involved = {wires[v] for v in trace(z) if v[0] not in 'xy'}
                involved = {v for v in trace(z) if v[0] not in 'xy'}
                bad.append(sorted(involved)[::-1])

        # print(actual_all)
        # print(expected_all)
        return sorted(bad, key=len)

    gs = find_invalid()

    # for i, g in enumerate(gs):
    #     print(i, g)
    # print()

    def analyze_zs():
        # Look for common patterns among gates
        z_ins = []
        for name, g in sorted(wires.items()):
            if isinstance(g, Gate):
                e, f = [
                    wires[n].op if isinstance(wires[n], Gate) else wires[n]
                    for n in (g.in1, g.in2)
                ]
                e, f = sorted([e, f])
                # print(name, e, f)
                z_ins.append(tuple(map(str, (e, g.op, f, name))))
                # print('    ', wires[g.in1])
                # print('    ', wires[g.in2])
                # print(
                #     '    ', wires[g.in2].op
                #     if isinstance(wires[g.in2], Gate) else wires[g.in2]
                # )

        for x in sorted(z_ins):
            print(x)

    def analyze_vs(ch: Literal['x', 'y']):
        y_outs = defaultdict(list)
        for name, gate in sorted(wires.items()):
            if not isinstance(gate, Gate):
                continue
            for i in gate.inputs:
                if i.startswith(ch):
                    y_outs[i].append(gate)

        grouped = defaultdict(list)

        for name, outs in sorted(y_outs.items()):
            t = tuple(sorted([out.op for out in outs]))
            grouped[t].append(name)

        for expr, names in sorted(grouped.items()):
            print('>>>', expr, ','.join(names))

    # analyze_zs()
    print('# X outputs:\n')
    analyze_vs('x')

    print('\n# Y outputs:\n')
    analyze_vs('y')

    exit()

    gates = list(set(g for gates in gs for g in gates))
    for selected in combinations(gates, r=8):
        possible_pairs = list(combinations(selected, 2))
        for swap_pairs in combinations(possible_pairs, 4):
            continue
            x, y = swap_pairs
            wires[x], wires[y] = wires[y], wires[x]
            if res := find_invalid():
                print(res)
            else:
                print('wooooo')
                exit(0)
            wires[x], wires[y] = wires[y], wires[x]

    print(gs)
    # for x,y in combinations(gs, r=2):
    #     if set(x) & set(y):
    #         print(x,y)
    exit(0)

    used = set()

    def dfs(bad, left=4, seq=tuple()):
        nonlocal used

        print(seq)

        if not bad:
            print(wires)
            return True

        if left == 0:
            return not bad

        gates = sorted({gate for group in bad for gate in group} - used)
        for a, b in combinations(gates, r=2):

            wires[a], wires[b] = wires[b], wires[a]
            used |= {a, b}

            try:
                newbad = find_invalid()
                if dfs(newbad, left - 1, seq + (a, b)):
                    return True
                # print(newbad)
            except LoopError:
                pass

            wires[a], wires[b] = wires[b], wires[a]
            used -= {a, b}

    # print(f'{x_value:>7b}')
    # print(f'{y_value:>7b}')
    # print('-'*7)
    # print(f'{z_value:>7b} expected')
    # print(f'{z_calc:>7b} actual')
    # print()
    # print(f'{x_value} + {y_value} = {z_value} (got {z_calc})')
    # print()

    bad = find_invalid()
    __import__('pprint').pprint(bad)

    try:
        success = dfs(bad)
        print(success)
    except RecursionError as exc:
        print('recursion error', exc)


# a1 = part1()
# print('part1:', a1)
# assert a1 == 65740327379952

a2 = part2()
print('part2:', a2)
