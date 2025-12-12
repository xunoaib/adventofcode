import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cache
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def toshape(lines):
    s = frozenset(
        (r, c) for r, line in enumerate(lines) for c, ch in enumerate(line)
        if ch == '#'
    )
    return settle(s)


def settle(s):
    rmin = min(r for r, c in s)
    cmin = min(c for r, c in s)

    if rmin == cmin == 0:
        return s

    return {(r - rmin, c - cmin) for r, c in s}


def tolines(shape):
    rmax = max(r for r, c in shape)
    cmax = max(c for r, c in shape)

    lines = []

    for r in range(rmax + 1):
        lines.append(
            ''.join('#' if (r, c) in shape else '.' for c in range(cmax + 1))
        )

    return lines


def shift(shape: frozenset[tuple[int, int]], offset: tuple[int, int]):
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


@cache
def ways_to_place(shape_idx, times):
    return _ways_to_place(shape_idx, times)


@cache
def _ways_to_place(shape_idx, times: int, used=frozenset()):
    if times == 0:
        return {
            used,
        }

    results = frozenset()
    for shape in shapesets[shape_idx]:
        if not shape & used:
            results |= _ways_to_place(shape_idx, times - 1, used | shape)
    return results


@cache
def permute_shape_region(shape, l, w) -> list[set[tuple[int, int]]]:
    results = []
    for rot in perm(shape):
        for roff in range(l - 2):
            for coff in range(w - 2):
                s = shift(rot, (roff, coff))
                if all(r < l and c < w for r, c in s):
                    results.append(s)
    return results


def part1():
    all_ways = []
    for idx, count in enumerate(counts):
        wtp = ways_to_place(idx, count)
        print(len(wtp))
        all_ways.append(wtp)

    print([len(x) for x in all_ways])
    return 1


def part1_old(self: Solver):

    @cache
    def solve(idx, used):
        if idx >= len(self.counts):
            return True

        if self.counts[idx] == 0:
            return solve(idx + 1, used)

        self.counts[idx] -= 1
        shape = shapes[idx]
        if not s & used and all(r < self.l and c < self.w for r, c in s):
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
aa = 0

for i, line in enumerate(elines):
    a, *counts = line.split()
    w, l = map(int, a[:-1].split('x'))
    counts = list(map(int, counts))

    area = w * l
    cellcount = sum(count * len(shape) for count, shape in zip(counts, shapes))

    if cellcount > area:
        # print(f'[{i}] Impossible area')
        continue

    aa += 1

    # wcount = w // 3
    # lcount = l // 3
    #
    # if wcount * lcount > sum(counts):
    #     print(f'[{i}] Sufficient 3x3')
    #     aa += 1
    #     continue

    # print()
    # print(f'[{i}] Processing {line}')
    # print(f'{area=}, {cellcount=}')
    # shapesets = [permute_shape_region(shape, l, w) for shape in shapes]
    # aa += part1()

# 245 too low

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
