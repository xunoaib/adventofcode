#!/usr/bin/env python3
# import copy
# import re
# import numpy as np
# from collections import defaultdict
# from itertools import permutations
import sys

L, R, U, D = (0,-1), (0,1), (-1,0), (1,0)

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

    return tuple()

states = set()

def part1(grid, visited, r, c, curdir):
    state = (r,c, curdir)
    if state in states:
        return
    states.add(state)

    visited.add((r,c))
    # while len(ndirs := nextdirs(grid.get((r,c)), curdir)) == 1:
    while True:
        ndirs = nextdirs(grid.get((r,c)), curdir)
        print(r, c, grid.get((r,c)), ndirs)
        if len(ndirs) != 1:
            break
        curdir = ndirs[0]
        r += curdir[0]
        c += curdir[1]
        if (r,c) not in grid:
            return
        visited.add((r,c))
    print('end', r, c, curdir)

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
    print('part1:', len(visited))

    # print('part1:', a1)
    # print('part2:', a2)

    # assert a1 == 0
    # assert a2 == 0

if __name__ == '__main__':
    main()
