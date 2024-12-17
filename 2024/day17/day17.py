#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)

ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = range(8)
A,B,C = range(3)

def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff and coff):
            yield r + roff, c + coff

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


r = [int(input().split(': ')[1]) for _ in range(3)]
input()
nums = eval('['+input().split(': ')[1]+']')

print(r)
print(nums)

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
    print(out)

print('part1:', ','.join(map(str, out)))
