import sys
from collections import Counter, defaultdict
from functools import cache
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


@cache
def reachable_keys(r, c, keys: frozenset[str] = frozenset()):
    '''Finds all reachable keys from the current tile'''

    OPEN_DOORS = {p for p in {DOOR_POS.get(k.upper()) for k in keys} if p}
    navigable = NAVIGABLE | OPEN_DOORS

    results = []

    q = [(r, c, 0)]
    visited = {(r, c)}
    while q:
        r, c, cost = q.pop(0)
        for np in neighbors4(r, c):
            if np not in visited and np in navigable:
                q.append((*np, cost + 1))
                visited.add(np)

                if np in KEYS and GRID[np] not in keys:
                    results.append((np, GRID[np], cost + 1))
                    keys = keys | {GRID[np]}

    return results


@cache
def shortest(r, c, keys: frozenset[str] = frozenset(), totcost=0):
    if len(keys) == len(KEYS):
        print('Done!', totcost)
        return 0

    results = list(reachable_keys(r, c, keys))
    if not results:
        print({p for p in {DOOR_POS.get(k.upper()) for k in keys} if p})
        print({DOOR_POS.get(k.upper()) for k in keys})
        print(keys)
        exit()

    assert results, f'Unsolvable: {(r,c)} with {"".join(sorted(keys))}'

    best = float('inf')
    for np, key, keycost in results:
        cost = keycost + shortest(*np, keys | {key}, totcost + keycost)
        # print(f'Cost = {cost}, Keys: {"".join(sorted(keys))}')
        best = min(best, cost)
    return best


lines = sys.stdin.read().strip().split('\n')
GRID = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

KEYS = {p for p, ch in GRID.items() if ch.islower()}
DOORS = {p for p, ch in GRID.items() if ch.isupper()}
EMPTY = {p for p, ch in GRID.items() if ch == '.'}
START_POS = next(p for p, ch in GRID.items() if ch == '@')
NAVIGABLE = KEYS | EMPTY | {START_POS}

DOOR_POS = {GRID[p]: p for p in DOORS}
KEY_POS = {GRID[p]: p for p in KEYS}


def main():
    a1 = a2 = 0

    a1 = shortest(*START_POS)
    print('part1:', a1)
    exit()


if __name__ == '__main__':
    main()
