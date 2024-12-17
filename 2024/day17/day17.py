#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import batched, pairwise, permutations, product

from z3 import (BitVec, BV2Int, If, Int, Int2BV, Ints, Optimize, Solver, sat,
                unsat)

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)

ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = range(8)
NAMES = 'ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV'.split(', ')
A,B,C = range(3)

ANNOTATIONS = {
    "ADV": "\033[93mA = A // 2**combo(operand)\033[0m",
    "BDV": "B = A // 2**combo(operand)",
    "CDV": "C = A // 2**combo(operand)",
    "BXL": "B ^= operand",
    "BXC": "B ^= C",
    "BST": "B = combo(operand) % 8",
    "JNZ": "\033[91mif A: pc = operand - 2\033[0m",
    "OUT": "\033[92mecho combo(operand) % 8\033[0m",
}

r = [int(input().split(': ')[1]) for _ in range(3)]
orig_r = r.copy()
input()
nums = eval('['+input().split(': ')[1]+']')

def literal(operand):
    return operand

def combo(operand):
    return {
        4: r[A],
        5: r[B],
        6: r[C],
        7: None,
    }.get(operand, operand)

def execute(pc):
    opcode = nums[pc]
    operand = nums[pc+1]

    if opcode == ADV:
        r[A] = int(r[A] / 2**combo(operand))
    elif opcode == BXL:
        r[B] = r[B] ^ literal(operand)
    elif opcode == BST:
        r[B] = combo(operand) % 8
    elif opcode == JNZ:
        if r[A] != 0:
            pc = literal(operand) - 2
    elif opcode == BXC:
        r[B] = r[B] ^ r[C]
    elif opcode == BXC:
        r[B] = r[B] ^ r[C]
    elif opcode == OUT:
        out.append(combo(operand) % 8)
    elif opcode == BDV:
        r[B] = int(r[A] / 2**combo(operand))
    elif opcode == CDV:
        r[C] = int(r[A] / 2**combo(operand))

    return pc + 2

pc = 0
out: list[int] = []
while pc in range(len(nums)):
    pc = execute(pc)

a1 = ','.join(map(str, out))
print('part1:', a1)
# assert a1 == '6,4,6,0,4,5,7,2,7'
# print()
# # ========================================

def execute2(pc):
    opcode = nums[pc]
    operand = nums[pc+1]

    if opcode == ADV:
        # r[A] = int(r[A] / 2**combo(operand))
        nra = makez(f'a{len(zas)}')
        solver.add(nra == zas[-1] / 2**combo(operand))
        zas.append(nra)
    elif opcode == BXL:
        # r[B] = r[B] ^ literal(operand)
        nrb = makez(f'b{len(zbs)}')
        solver.add(nrb == zbs[-1] ^ literal(operand))
        zbs.append(nrb)
    elif opcode == BST:
        # r[B] = combo(operand) % 8
        nrb = makez(f'b{len(zbs)}')
        solver.add(nrb == combo(operand) % 8)
        zbs.append(nrb)
    elif opcode == JNZ:
        # TODO:
        print('branch!', pc)
        solve()
        if r[A] != 0:
            pc = literal(operand) - 2
        exit(0)
    elif opcode == BXC:
        # r[B] = r[B] ^ r[C]
        nrb = makez(f'b{len(zbs)}')
        solver.add(nrb == zbs[-1] ^ zcs[-1])
        zbs.append(nrb)
    elif opcode == OUT:
        # TODO:
        out.append(combo(operand) % 8)
    elif opcode == BDV:
        # r[B] = int(r[A] / 2**combo(operand))
        nrb = makez(f'b{len(zbs)}')
        solver.add(nrb == zas[-1] / 2**combo(operand))
        zbs.append(nrb)
    elif opcode == CDV:
        # r[C] = int(r[A] / 2**combo(operand))
        nrc = makez(f'c{len(zcs)}')
        solver.add(nrc == zas[-1] / 2**combo(operand))
        zbs.append(nrc)

    return pc + 2

def solve():

    print(f'{zas=}')
    print(f'{zbs=}')
    print(f'{zcs=}')

    solver.minimize(zas[0])

    if solver.check() == unsat:
        print('unsat')
        return

    m = solver.model()
    print(m[zas[0]].as_long())

    # while solver.check() == sat:
    #     m = solver.model()
    #     print(m[zas[0]].as_long())
    #     solver.add(zas[0] != m[zas[0]].as_long())

def makez(n):
    return BitVec(n, 32)

print(nums)
print()
print(', '.join(NAMES[n] for n in nums))

for i, (opcode, operand) in enumerate(batched(nums, 2)):
    anno = ANNOTATIONS[NAMES[opcode]]
    # anno = anno.replace('combo(operand)', str(combo(operand)))
    anno = anno.replace('operand', str(operand))
    anno = anno.replace('combo(0)', '0')
    anno = anno.replace('combo(1)', '1')
    anno = anno.replace('combo(2)', '2')
    anno = anno.replace('combo(3)', '3')
    anno = anno.replace('combo(4)', 'A')
    anno = anno.replace('combo(5)', 'B')
    anno = anno.replace('combo(6)', 'C')

    print(f'{i:>2}  {NAMES[opcode]}  {operand}      {anno}')

exit(0)
pc = 0
out = []
r = orig_r.copy()

# zr = Ints('a0 b0 c0')
zr = [makez(f'{n}0') for n in 'abc']
zas = [zr[0]]
zbs = [zr[1]]
zcs = [zr[2]]

solver = Optimize()
# solver.add(zas[-1] == r[A])
solver.add(zbs[-1] == r[B])
solver.add(zcs[-1] == r[C])

while pc in range(len(nums)):
    pc = execute2(pc)


solve()
