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

    # Create initial walkable graph
    edges: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for p in walkable:
        for n in neighbors4(*p):
            if n in walkable:
                edges[p].add(n)
                edges[n].add(p)

    telepoints = defaultdict(set)

    for p in telepads:
        n = next(n for n in neighbors4(*p) if n in telepads)

        # Find 2-letter teleporter ID
        tkey = ''.join(sorted(grid[p] + grid[n]))

        # Find empty passages connected to each teleporter
        telepoints[tkey].add(
            next(t for s in (p, n) for t in neighbors4(*s) if t in walkable)
        )

    # Find start and end locations
    start = telepoints.pop('AA').pop()
    end = telepoints.pop('ZZ').pop()

    # Add edges between teleporters
    for tkey, (p, n) in telepoints.items():
        edges[p].add(n)
        edges[n].add(p)


if __name__ == '__main__':
    main()
