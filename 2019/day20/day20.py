import sys
from collections import defaultdict


def neighbors4(r: int, c: int):
    for roff, coff in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yield r + roff, c + coff


def main():
    lines = sys.stdin.read().splitlines()

    grid = {
        (r, c): v
        for r, line in enumerate(lines)
        for c, v in enumerate(line) if v != ' '
    }

    walkable = {p for p, v in grid.items() if v == '.'}
    telepads = {p for p, v in grid.items() if v not in '.#'}

    padgroups = {}
    for p in telepads:
        n = next(n for n in neighbors4(*p) if n in telepads)
        key = ''.join(sorted(grid[p] + grid[n]))
        padgroups[key] = (p, n)

    print(padgroups)
    exit()

    print([grid[p] for p in telepads])

    counts = {0: 0, 1: 0}
    for p in telepads:
        s = sum(grid.get(n) == '.' for n in neighbors4(*p))
        counts[s] += 1
        if s not in (0, 1):
            print(s)

    print(counts)


if __name__ == '__main__':
    main()
