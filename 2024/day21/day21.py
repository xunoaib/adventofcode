#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import pairwise, permutations, product
from typing import Any

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)

char_dirs = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0),
}

def add(a, b):
    return a[0]+b[0], a[1]+b[1]

def sub(a, b):
    return b[0]-a[0], b[1]-a[1]

numeric_chars = '789\n456\n123\n.0A'
directional_chars = '.^A\n<v>'

numeric_grid = {
    (r, c): ch
    for r, line in enumerate(numeric_chars.split('\n'))
    for c, ch in enumerate(line)
    if ch != '.'
}

directional_grid = {
    (r, c): ch
    for r, line in enumerate(directional_chars.split('\n'))
    for c, ch in enumerate(line)
    if ch != '.'
}

numeric_start = next(p for p, ch in numeric_grid.items() if ch == 'A')
directional_start = next(p for p, ch in directional_grid.items() if ch == 'A')

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff

class Keypad:
    def __init__(self, grid):
        self.grid = grid

    def push(self, pos):
        if pos not in self.grid:
            raise IndexError('Out of bounds:', pos)
        return self.grid[pos]

    def items(self):
        return self.grid.items()

class NumericKeypad(Keypad):
    def __init__(self):
        super().__init__(numeric_grid)

class DirectionalKeypad(Keypad):
    def __init__(self):
        super().__init__(directional_grid)

class WrappedKeypad():
    def __init__(self, inner: 'Keypad | WrappedKeypad', outer: Keypad):
        self.outer = outer
        self.inner = inner
        self.inner_pos = next(p for p, ch in self.inner.items() if ch == 'A')

    def items(self):
        print('called items on', self, self.outer)
        return self.outer.items()

kp_num = NumericKeypad()
kp_dir1 = WrappedKeypad(kp_num, DirectionalKeypad())
kp_dir2 = WrappedKeypad(kp_dir1, DirectionalKeypad())
kp_dir3 = WrappedKeypad(kp_dir2, DirectionalKeypad())

# print(kp_num.inner_pos)
print(kp_dir1.inner_pos)
print(kp_dir2.inner_pos)
print(kp_dir3.inner_pos)

@dataclass
class Simulation:
    keypads = [DirectionalKeypad(), DirectionalKeypad(), DirectionalKeypad(), NumericKeypad()]

    def push(self, ch):
        pass


def dist_to(src, tar):
    a, b = sub(src, tar)
    return abs(a) + abs(b)

def pos_of_char(grid, search_ch):
    return next(p for p, ch in grid.items() if ch == search_ch)

def numeric_dists(code, start_pos):
    positions = [start_pos] + [pos_of_char(numeric_grid, ch) for ch in code]
    dists = [dist_to(a, b) for a,b in pairwise(positions)]

codes = sys.stdin.read().strip().split('\n')

for code in codes:
    print(code)

    numeric_pos = numeric_start
    dists = numeric_dists(code, numeric_pos)

    exit(0)
