import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cache
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def toshape(lines):
    return {
        (r, c)
        for r, line in enumerate(lines)
        for c, ch in enumerate(line) if ch == '#'
    }


def tolines(shape):
    rmax = max(r for r, c in shape)
    cmax = max(c for r, c in shape)

    lines = []

    for r in range(rmax + 1):
        lines.append(
            ''.join('#' if (r, c) in shape else '.' for c in range(cmax + 1))
        )

    return lines


def shift(shape: set[tuple[int, int]], offset: tuple[int, int]):
    return {(r + offset[0], c + offset[1]) for r, c in shape}


def rotate_cw(mat: list):
    return [list(row) for row in zip(*mat[::-1])]


def rotate_ccw(mat: list):
    return [list(row) for row in zip(*mat)][::-1]


def rotshape(shape):
    return toshape(rotate_cw(tolines(shape)))


def printset(shape):
    print(*tolines(shape), sep='\n')


def perm(shape):
    for _ in range(4):
        yield shape
        shape = rotshape(shape)


@dataclass
class Solver:
    w: int
    l: int
    counts: list[int]


def part1(self: Solver):

    @cache
    def solve(idx, used):
        if idx >= len(self.counts):
            return True

        if self.counts[idx] == 0:
            return solve(idx + 1, used)

        self.counts[idx] -= 1
        shape = shapes[idx]
        for rot in perm(shape):
            for roff in range(self.l - 2):
                for coff in range(self.w - 2):
                    s = shift(rot, (roff, coff))
                    if not s & used and all(
                        r < self.l and c < self.w for r, c in s
                    ):
                        if solve(idx, used | s):
                            return True

        self.counts[idx] += 1
        return False

    return solve(0, frozenset())


s = sys.stdin.read().strip()
*gs, end = s.split('\n\n')

shapes = []
for i, g in enumerate(gs):
    lines = g.split('\n')[1:]
    shape = toshape(lines)
    shapes.append(shape)

elines = end.split('\n')

for line in elines:
    a, *counts = line.split()
    w, l = map(int, a[:-1].split('x'))
    counts = list(map(int, counts))
    s = Solver(w, l, counts)
    print(part1(s))

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
