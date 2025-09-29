import sys
from itertools import product
from typing import Generator

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors8(r: int, c: int) -> Generator[tuple[int, int]]:
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff == coff == 0):
            yield r + roff, c + coff


def count_on_neighbors(r: int, c: int):
    return len(set(neighbors8(r, c)) & on)


lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

all_coords = list(grid)
on: set[tuple[int, int]] = {p for p, ch in grid.items() if ch == '#'}

for _ in range(100):
    on = {
        p
        for p in all_coords if (
            (p in on and count_on_neighbors(*p) in [2, 3]) or
            (p not in on and count_on_neighbors(*p) == 3)
        )
    }

a1 = len(on)

print('part1:', a1)

assert a1 == 814
