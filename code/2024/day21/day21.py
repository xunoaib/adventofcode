#!/usr/bin/env python3
import sys
from functools import cache
from itertools import pairwise


def find_path(v1: str, v2: str):
    numpad = is_numpad(v1) or is_numpad(v2)
    grid, corner = (NUM_GRID, (3, 0)) if numpad else (DIR_GRID, (0, 0))
    r1, c1 = grid[v1]
    r2, c2 = grid[v2]

    hchar = '>' if c2 > c1 else '<'
    vchar = 'v' if r2 > r1 else '^'

    path = hchar * abs(c2 - c1) + vchar * abs(r2 - r1)
    path = ''.join(sorted(path, key='>v^<'.index))

    return path[::-1] if corner not in [(r2, c1), (r1, c2)] else path


@cache
def path_length(path: str, depth: int):
    if depth < 0:
        return len(path) + 1

    return sum(
        path_length(find_path(a, b), depth - 1)
        for a, b in pairwise(f'A{path}A'))


def solve(length: int):
    return sum(path_length(code[:3], length) * int(code[:3]) for code in codes)


def is_numpad(char: str):
    return char in '0123456789'


def to_charpos_dict(chars: str):
    return {
        ch: (r, c)
        for r, line in enumerate(chars.split('\n'))
        for c, ch in enumerate(line) if ch != '.'
    }


NUM_GRID = to_charpos_dict('789\n456\n123\n.0A')
DIR_GRID = to_charpos_dict('.^A\n<v>')

codes = sys.stdin.read().strip().split('\n')

a1 = solve(2)
a2 = solve(25)

print('part1:', a1)
print('part2:', a2)

assert a1 == 213536
assert a2 == 258369757013802
