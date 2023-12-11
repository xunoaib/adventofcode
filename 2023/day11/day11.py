#!/usr/bin/env python3
import copy
from itertools import permutations
import sys

def main():
    lines = sys.stdin.read().strip().split('\n')

    nlines = []
    for r, line in enumerate(lines):
        if set(line) == {'.'}:
            nlines += [line]*2
        else:
            nlines.append(line)

    lines = copy.deepcopy(nlines)
    nlines = [[] for _ in range(len(lines))]
    for c in range(len(lines[0])):
        if set(line[c] for line in lines) == {'.'}:
            for r, line in enumerate(lines):
                nlines[r] += ['.'] * 2
        else:
            for r, line in enumerate(lines):
                nlines[r].append(line[c])

    galaxies = sorted({(r,c) for r, line in enumerate(nlines) for c, ch in enumerate(line) if ch == '#'})
    print(galaxies)

    ans1 = 0
    for a,b in permutations(galaxies, r=2):
        diff = abs(a[0] - b[0]) + abs(a[1] - b[1])
        ans1 += diff

    print('part1:', ans1//2)

if __name__ == '__main__':
    main()
