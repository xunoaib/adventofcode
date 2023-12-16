#!/usr/bin/env python3
import sys

DIRS = L, R, U, D = (0,-1), (0,1), (-1,0), (1,0)

states = set()

def nextdirs(ch, curdir):
    if ch == '.':
        return (curdir,)
    if ch == '-':
        if curdir in (L, R):
            return (curdir,)
        return (L, R)
    if ch == '|':
        if curdir in (U, D):
            return (curdir,)
        return (U, D)
    if ch == '/':
        return {
            L: (D,),
            U: (R,),
            R: (U,),
            D: (L,),
        }[curdir]
    if ch == '\\':
        return {
            L: (U,),
            U: (L,),
            R: (D,),
            D: (R,),
        }[curdir]

def part1(grid, visited, r, c, curdir):
    state = (r,c, curdir)
    if state in states:
        return
    states.add(state)

    visited.add((r,c))
    while True:
        ndirs = nextdirs(grid.get((r,c)), curdir)
        if len(ndirs) != 1:
            break
        curdir = ndirs[0]
        r += curdir[0]
        c += curdir[1]
        if (r,c) not in grid:
            return
        visited.add((r,c))

    for ndir in ndirs:
        roff, coff = ndir
        npos = nr, nc = r+roff, c+coff
        if npos in grid:
            part1(grid, visited, nr, nc, ndir)

def main():
    lines = sys.stdin.read().strip().split('\n')

    g = {}
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            g[r, c] = ch

    visited = set()
    r,c = pos = (0, 0)
    roff, coff = curdir = R
    part1(g,visited,r,c,curdir)
    a1 = len(visited)
    print('part1:', a1)

    rs, cs = zip(*g)
    maxr = max(rs)
    maxc = max(cs)

    points = [(r, 0) for r in range(maxr+1)]
    points += [(r, maxc) for r in range(maxr+1)]
    points += [(0, c) for c in range(maxc+1)]
    points += [(maxr, c) for c in range(maxc+1)]
    points = set(points)

    a2 = 0
    for d in DIRS:
        for r,c in points:
            states.clear()
            visited = set()
            curdir = R
            part1(g,visited,r,c,d)
            a2 = max(a2, len(visited))
    print('part2:', a2)

    assert a1 == 6622
    assert a2 == 7130

if __name__ == '__main__':
    main()
