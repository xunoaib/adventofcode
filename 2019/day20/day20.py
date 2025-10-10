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

    telepoints = defaultdict(set)

    for p in telepads:
        n = next(n for n in neighbors4(*p) if n in telepads)

        # Find 2-letter teleporter ID
        tkey = ''.join(sorted(grid[p] + grid[n]))

        # Find empty passages connected to each teleporter
        telepoints[tkey].add(
            next(t for s in (p, n) for t in neighbors4(*s) if t in walkable)
        )

    print(telepoints)


if __name__ == '__main__':
    main()
