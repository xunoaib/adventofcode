#!/usr/bin/env python3
import sys
from collections import defaultdict
from itertools import pairwise

DIRS = U, R, D, L = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIAGS = DL, DR, UL, UR = [(1, -1), (1, 1), (-1, -1), (-1, 1)]


def flip(direction):
    return DIRS[(DIRS.index(direction) + 2) % len(DIRS)]


SYMDIRS = {
    '|': (U, D),
    '-': (L, R),
    'L': (U, R),
    'J': (L, U),
    '7': (L, D),
    'F': (R, D),
}

# maps character to [left_rel_positions, right_rel_positions]
# designate relative tile positions to be considered to the "left" or "right"
# of each tile type when the tile has been entered from a given direction
SIDES = {
    '|': {
        U: ((L, ), (R, ))
    },
    '-': {
        R: ((U, ), (D, ))
    },
    'F': {
        U: ((L, U), (DR, )),
    },
    'J': {
        R: ((UL, ), (D, R)),
    },
    '7': {
        R: ((U, R), (DL, ))
    },
    'L': {
        D: ((UR, ), (D, L))
    }
}

# swap and add left/right designations when moving in the opposite pipe direction from above
for ch, dirs in SYMDIRS.items():
    val = tuple(SIDES[ch].values())[0]
    for d in dirs:
        if flip(d) not in SIDES[ch]:
            SIDES[ch][flip(d)] = val[::-1]


def neighbors(r, c):
    yield r + 1, c
    yield r - 1, c
    yield r, c - 1
    yield r, c + 1


def makegraph(grid):
    cs = defaultdict(set)
    for p1, ch1 in grid.items():
        r, c = p1
        for d in SYMDIRS[ch1]:
            p2 = (r + d[0], c + d[1])
            if ch2 := grid.get(p2):
                dirs2 = SYMDIRS[ch2]
                if flip(d) in dirs2:
                    cs[p2].add((r, c))
                    cs[(r, c)].add(p2)
    return cs


def findpath(graph, spos):
    visited = {spos}
    q = [spos]
    p = None
    path = []
    while q:
        p = q.pop(0)
        path.append(p)
        if p2 := next((n for n in graph[p] if n not in visited), None):
            visited.add(p2)
            q.append(p2)
        else:
            break

    if graph[p] == {path[-2], path[0]}:
        return len(path) // 2, path
    return 0, []


def getpool(grid, pos):

    max_r = max(r for r, _ in grid)
    max_c = max(c for _, c in grid)
    min_r = min(r for r, _ in grid)
    min_c = min(c for _, c in grid)

    pool = {pos}
    visited = {pos}
    q = [pos]

    while q:
        p = q.pop()
        for p2 in neighbors(*p):
            r2, c2 = p2
            if p2 in visited:
                continue
            visited.add(p2)
            if not (min_r <= r2 <= max_r and min_c <= c2 <= max_c):
                continue
            if not grid.get(p2):
                pool.add(p2)
                q.append(p2)
    return pool


def part2(grid, path):
    # remove irrelevant/unused pipes
    for p in list(grid):
        if p not in path:
            del grid[p]

    path.append(path[0])
    left, right = set(), set()

    for p1, p2 in pairwise(path):
        vec = tuple(y - x for x, y in zip(p1, p2))
        ch2 = grid[p2]
        leftpos, rightpos = SIDES[ch2][vec]

        for roff, coff in leftpos:
            p3 = p2[0] + roff, p2[1] + coff
            if not grid.get(p3):
                left.add(p3)

        for roff, coff in rightpos:
            p3 = p2[0] + roff, p2[1] + coff
            if not grid.get(p3):
                right.add(p3)

    leftpool = set()
    for p in left:
        leftpool |= getpool(grid, p)

    rightpool = set()
    for p in right:
        rightpool |= getpool(grid, p)

    return min(len(leftpool), len(rightpool))


def main():
    lines = sys.stdin.read().strip().split('\n')

    grid = {
        (r, c): v
        for r, row in enumerate(lines)
        for c, v in enumerate(row) if v != '.'
    }
    spos = next(p for p, v in grid.items() if v == 'S')

    for ch in SYMDIRS:
        grid[spos] = ch
        graph = makegraph(grid)
        if len(graph[spos]) == 2:
            ans1, path = findpath(graph, spos)
            print('part1:', ans1)
            ans2 = part2(grid, path)
            print('part2:', ans2)

            assert ans1 == 6733
            assert ans2 == 435
            break


if __name__ == '__main__':
    main()
