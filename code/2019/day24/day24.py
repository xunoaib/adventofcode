import sys

DIRS = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    return {(r + roff, c + coff) for roff, coff in DIRS}


aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

ROWS = max(r for r, _ in grid) + 1

bugs = frozenset(p for p, ch in grid.items() if ch == '#')
alltiles = set(grid)
seen = set()

while bugs not in seen:
    seen.add(bugs)
    bugs = frozenset(
        p for p in alltiles
        if len(neighbors4(*p) & bugs) in (1, 1 + (p not in bugs))
    )

aa = sum(2**(r * ROWS + c) for r, c in bugs)

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

assert aa == 17863741
# assert bb == 0
