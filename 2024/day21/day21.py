#!/usr/bin/env python3
import sys
from functools import cache
from itertools import pairwise


def find_path(v1: str, v2: str):
    numpad = is_numpad(v1) or is_numpad(v2)
    grid_pos = ngrid_pos if numpad else dgrid_pos
    corner_pos = (3, 0) if numpad else (0, 0)
    r1, c1 = grid_pos[v1]
    r2, c2 = grid_pos[v2]

    hchar = '>' if c2 > c1 else '<'
    vchar = 'v' if r2 > r1 else '^'

    path = hchar * abs(c2 - c1) + vchar * abs(r2 - r1)
    path = ''.join(sorted(path, key=lambda c: '>v^<'.index(c)))

    if corner_pos not in [(r2, c1), (r1, c2)]:
        path = path[::-1]

    return path


@cache
def path_length(seq: str, depth: int):
    if depth < 0:
        return len(seq) + 1

    t = 0
    for v1, v2 in pairwise(f'A{seq}A'):
        t += path_length(find_path(v1, v2), depth - 1)
    return t


def is_numpad(char: str):
    return char in '0123456789'


numeric_chars = '789\n456\n123\n.0A'
directional_chars = '.^A\n<v>'

ngrid = numeric_grid = {
    (r, c): ch
    for r, line in enumerate(numeric_chars.split('\n'))
    for c, ch in enumerate(line) if ch != '.'
}

dgrid = directional_grid = {
    (r, c): ch
    for r, line in enumerate(directional_chars.split('\n'))
    for c, ch in enumerate(line) if ch != '.'
}

ngrid_pos = {ch: pos for pos, ch in ngrid.items()}
dgrid_pos = {ch: pos for pos, ch in dgrid.items()}


def part1_new():
    codes = sys.stdin.read().strip().split('\n')
    a1 = 0
    for code in codes:
        a = path_length(code[:3], 2)
        b = int(code[:3])
        print(a, b)
        print()
        a1 += a * b
    print(a1)


if __name__ == "__main__":
    part1_new()
