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


for i, (opcode, operand) in enumerate(batched(nums, 2)):
    anno = ANNOTATIONS[NAMES[opcode]]
    anno = anno.replace('operand', str(operand))
    anno = anno.replace('combo(0)', '0')
    anno = anno.replace('combo(1)', '1')
    anno = anno.replace('combo(2)', '2')
    anno = anno.replace('combo(3)', '3')
    anno = anno.replace('combo(4)', 'A')
    anno = anno.replace('combo(5)', 'B')
    anno = anno.replace('combo(6)', 'C')

    print(f'{i:>2}:  {NAMES[opcode]} {operand}    {anno}')
