#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product
from time import time

from z3 import BitVec, BV2Int, If, Int, Int2BV, Ints, Solver, sat, unsat

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)

ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = range(8)
NAMES = 'ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV'.split(', ')
A,B,C = range(3)

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
        v = combo(operand) % 8
        if len(out) == len(nums) or v != nums[len(out)]:
            return -1
        out.append(v)
    elif opcode == BDV:
        r[B] = int(r[A] / 2**combo(operand))
    elif opcode == CDV:
        r[C] = int(r[A] / 2**combo(operand))

    return pc + 2

def solve(init_a):
    global pc, out, r
    r = orig_r.copy()
    r[A] = init_a
    pc = 0
    out = []

    while pc in range(len(nums)):
        pc = execute(pc)

    if out == nums:
        return True

last = time()

a = 4742306
while True:
    if solve(a):
        print('part2:', a)
        break
    if time() - last > 1:
        last = time()
        print(a)
    a += 1
