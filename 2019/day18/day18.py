import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


def reachable_keys(r, c, keys: set[str] = set()):
    '''Finds all reachable keys from the current tile'''

    navigable = NAVIGABLE | {DOOR_POS[k.upper()] for k in keys}

    q = [(r, c, 0)]
    visited = {(r, c)}
    while q:
        r, c, cost = q.pop(0)
        for np in neighbors4(r, c):
            if np not in visited and np in navigable:
                q.append((*np, cost + 1))
                visited.add(np)

                if np in KEYS and GRID[np] not in keys:
                    yield np, GRID[np], cost + 1
                    keys = keys | {GRID[np]}


lines = sys.stdin.read().strip().split('\n')
GRID = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

KEYS = {p for p, ch in GRID.items() if ch.islower()}
DOORS = {p for p, ch in GRID.items() if ch.isupper()}
EMPTY = {p for p, ch in GRID.items() if ch == '.'}
NAVIGABLE = KEYS | EMPTY

DOOR_POS = {GRID[p]: p for p in DOORS}
KEY_POS = {GRID[p]: p for p in KEYS}

start_pos = next(p for p, ch in GRID.items() if ch == '@')


def main():
    a1 = a2 = 0

    nodes = list(reachable_keys(*start_pos))
    keys = {n[1]
            for n in nodes} | set('ha') | set('lc') | set('ft') | set(
                'gez'
            ) | set('oqyu') | set('p') | set('wvx')

    for p in reachable_keys(*start_pos, keys):
        print(p)


if __name__ == '__main__':
    main()
