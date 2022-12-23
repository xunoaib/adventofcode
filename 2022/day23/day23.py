#!/usr/bin/env python3
import sys
from collections import defaultdict

N = (-1, 0)
NE = (-1, 1)
NW = (-1, -1)
S = (1, 0)
SE = (1, 1)
SW = (1, -1)
W = (0, -1)
E = (0, 1)


def getnext(elves, r, c, start_idx):
    dirchecks = [
        ([N, NE, NW], (r - 1, c)),
        ([S, SE, SW], (r + 1, c)),
        ([W, NW, SW], (r, c - 1)),
        ([E, NE, SE], (r, c + 1)),
    ]

    if all((r + roff, c + coff) not in elves for roff, coff in [N, NE, NW, S, SE, SW, W, E]):
        return r, c

    for i in range(4):
        offsets, newpos = dirchecks[(i + start_idx) % 4]
        if all((r + roff, c + coff) not in elves for roff, coff in offsets):
            return newpos

    return r, c


def step(elves, start_idx):
    target_elves = defaultdict(set)  # target => [elves, ...]
    for r, c in elves:
        tar = getnext(elves, r, c, start_idx)
        target_elves[tar].add((r, c))

    new_elves = set()
    for tar, elfset in list(target_elves.items()):
        if len(elfset) == 1:
            new_elves.add(tar)
        else:
            new_elves |= elfset

    return new_elves, (start_idx + 1) % 4


def count_ground(elves):
    minr = min(r for r, c in elves)
    minc = min(c for r, c in elves)
    maxr = max(r for r, c in elves)
    maxc = max(c for r, c in elves)

    count = 0
    for r in range(minr, maxr + 1):
        for c in range(minc, maxc + 1):
            if (r, c) not in elves:
                count += 1

    return count


def main():
    lines = sys.stdin.read().strip().split('\n')

    elves = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '#':
                elves.add((r, c))

    rounds = 1
    start_idx = 0
    ans1 = None

    while True:
        new_elves, start_idx = step(elves, start_idx)
        if rounds == 10:
            ans1 = count_ground(new_elves)
        if new_elves == elves:
            break
        elves = new_elves
        rounds += 1

    print('part1:', ans1)
    print('part2:', rounds)

    assert ans1 == 3800
    assert rounds == 916


if __name__ == '__main__':
    main()
