import sys
from collections.abc import Generator
from itertools import product


def neighbors8(r: int, c: int) -> Generator[tuple[int, int]]:
    for roff, coff in product([-1, 0, 1], repeat=2):
        if not (roff == coff == 0):
            yield r + roff, c + coff


def count_on_neighbors(r: int, c: int, on: set[tuple[int, int]]):
    return len(set(neighbors8(r, c)) & on)


def part1(on: set[tuple[int, int]]):
    for _ in range(100):
        on = {
            p
            for p in grid
            if (p in on and count_on_neighbors(*p, on) in [2, 3]) or
            (p not in on and count_on_neighbors(*p, on) == 3)
        }

    return len(on)


def part2(on: set[tuple[int, int]]):
    maxr = max(r for r, _ in grid)
    maxc = max(c for _, c in grid)

    ALWAYS_ON = {(0, 0), (0, maxc), (maxr, 0), (maxr, maxc)}

    on |= ALWAYS_ON
    for _ in range(100):
        on = {
            p
            for p in grid
            if (p in on and count_on_neighbors(*p, on) in [2, 3]) or
            (p not in on and count_on_neighbors(*p, on) == 3)
        } | ALWAYS_ON

    return len(on)


def main():
    global grid

    lines = sys.stdin.read().strip().split('\n')

    grid = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
    }

    on: set[tuple[int, int]] = {p for p, ch in grid.items() if ch == '#'}

    a1 = part1(on.copy())
    a2 = part2(on.copy())

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 814
    assert a2 == 924


if __name__ == '__main__':
    main()
