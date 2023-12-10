#!/usr/bin/env python3
import sys
from collections import defaultdict
from heapq import heappush, heappop

DIRS = U, R, D, L = [(-1, 0), (0, 1), (1, 0), (0, -1)]

SYMDIRS = {
    '|': (U, D),
    '-': (L, R),
    'L': (U, R),
    'J': (L, U),
    '7': (L, D),
    'F': (R, D),
}


def flip(direction):
    return DIRS[(DIRS.index(direction) + 2) % len(DIRS)]


def neighbors(r, c):
    yield r + 1, c
    yield r - 1, c
    yield r, c - 1
    yield r, c + 1


def makegraph(grid):
    cs = defaultdict(set)
    for p1, ch1 in grid.items():
        r, c = p1
        # for ch2, dirs in SYMDIRS.items():
        # print(ch1, SYMDIRS[ch1])
        for d in SYMDIRS[ch1]:
            p2 = (r + d[0], c + d[1])
            if ch2 := grid.get(p2):
                dirs2 = SYMDIRS[ch2]
                if flip(d) in dirs2:
                    cs[p2].add((r, c))
                    cs[(r, c)].add(p2)

    return cs


def findpath(grid, graph, spos):
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

def getpool(grid, pos, path):

    max_r = max(r for r,c in grid)
    max_c = max(c for r,c in grid)
    min_r = min(r for r,c in grid)
    min_c = min(c for r,c in grid)

    pool = {pos}
    borders = set()
    visited = {pos}
    valid = True
    q = [pos]

    while q:
        p = q.pop()
        for p2 in neighbors(*p):
            r2, c2 = p2

            if p2 in visited:
                continue
            visited.add(p2)

            # out of bounds
            if not (min_r <= r2 <= max_r and min_c <= c2 <= max_c):
                valid = False
                continue

            if ch2 := grid.get(p2):
                # unexpected border
                if p2 not in path:
                    valid = False
            else:
                # empty space, continue
                pool.add(p2)
                q.append(p2)
    return pool, valid

# CHSIDES = {
#     '|': ((L,),(R,)),
#     '-': ((U,),(D,)),
# }

def getleft(grid, r,c):
    ch = grid[r,c]

def part2(grid, g, path):
    adj = list({n for p in path for n in neighbors(*p) if not grid.get(n)})

    # left, right = set(), set()
    # print(path)

    # valid_set = set()
    # for p in adj:
    #     print(p)
    #     pool, valid = getpool(grid, p, path)
    #     if valid:
    #         print(pool)
    #         valid_set |= pool
    # print('xxx', len(valid_set), sorted(valid_set))

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
        g = makegraph(grid)
        if len(g[spos]) == 2:
            ans1, path = findpath(grid, g, spos)
            print('part1:', ans1)
            ans2 = part2(grid, g, path)

    # ans1 = part1(lines)
    # print('part1:', ans1)

    # ans2 = part2(lines)
    # print('part2:', ans2)

    # assert ans1 == 0
    # assert ans2 == 0


if __name__ == '__main__':
    main()
