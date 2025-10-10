import sys
from collections import defaultdict
from typing import TypeAlias

Pos: TypeAlias = tuple[int, int]


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
    edges: dict[Pos, set[Pos]] = defaultdict(set)

    for p in walkable:
        for n in neighbors4(*p):
            if n in walkable:
                edges[p].add(n)
                edges[n].add(p)

    telepoints: dict[str, set[Pos]] = defaultdict(set)

    for p in telepads:
        n = next(n for n in neighbors4(*p) if n in telepads)

        # Find 2-letter teleporter ID
        tkey = ''.join(sorted(grid[p] + grid[n]))

        # Find empty passages connected to each teleporter
        telepoints[tkey].add(
            next(t for s in (p, n) for t in neighbors4(*s) if t in walkable)
        )

    # Find start and end locations
    AA: Pos = telepoints.pop('AA').pop()
    ZZ: Pos = telepoints.pop('ZZ').pop()

    # Add edges between teleporters
    for tkey, (p, n) in telepoints.items():
        edges[p].add(n)
        edges[n].add(p)

    q = [(AA)]
    seen = {AA: 0}

    while q:
        p = q.pop(0)
        for n in edges[p]:
            print(n)
            if n not in seen:
                seen[n] = seen[p] + 1
                q.append(n)

    print('part1:', seen[ZZ])


if __name__ == '__main__':
    main()
