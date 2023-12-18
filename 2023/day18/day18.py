#!/usr/bin/env python3
import enum
import re
import sys

DIRS = U, D, L, R = [(-1, 0), (1, 0), (0, -1), (0, 1)]

cdirs = {'U': U, 'L': L, 'R': R, 'D': D}


def neighbors(r, c):
    for roff, coff in DIRS:
        yield r + roff, c + coff


def getbounds(s):
    rs, cs = zip(*s)
    minr, maxr = min(rs), max(rs)
    minc, maxc = min(cs), max(cs)
    return minr, maxr, minc, maxc


def getpool(border, r, c):
    minr, maxr, minc, maxc = getbounds(border)

    minr -= 1
    minc -= 1
    maxr += 1
    maxc += 1

    assert r, c not in border
    q = [(r, c)]
    pool = {(r, c)}
    seen = {(r, c)}

    while q:
        r, c = q.pop()
        if (r, c) in border:
            continue
        for nr, nc in neighbors(r, c):
            if (nr, nc) in seen or (nr, nc) in pool:
                continue
            seen.add((nr, nc))
            if minr <= nr <= maxr and minc <= nc <= maxc and (
                    nr, nc) not in border:
                pool.add((nr, nc))
                q.append((nr, nc))
    return pool


def print_lagoon(lagoon):
    minr, maxr, minc, maxc = getbounds(lagoon)
    for r in range(minr, maxr + 1):
        for c in range(minc, maxc + 1):
            ch = '#' if (r, c) in lagoon else '.'
            print(ch, end='')
        print()


def main():
    lines = sys.stdin.read().strip().split('\n')

    r, c = 0, 0
    lagoon = {(r, c)}

    for line in lines:
        d, count, h = re.search(r'(.*) (.*) \(#(.*)\)', line).groups()
        roff, coff = cdirs[d]
        for _ in range(int(count)):
            r, c = r + roff, c + coff
            lagoon.add((r, c))

    minr, maxr, minc, maxc = getbounds(lagoon)

    # find all open spots adjacent to the border
    adjopen = set()
    for r, c in lagoon:
        for nr, nc in neighbors(r, c):
            if (nr, nc) in lagoon and (nr, nc) not in adjopen:
                continue
            if minr <= nr <= maxr and minc <= nc <= maxc:
                adjopen.add((nr, nc))

    # find one pool
    pools = []
    adjopen = list(adjopen)
    while adjopen:
        r, c = adjopen.pop()
        newpool = getpool(lagoon, r, c)
        for i, p in enumerate(pools):
            if newpool & p:
                pools[i] |= newpool
                break
        else:
            pools.append(newpool)
        adjopen = list(set(adjopen) - newpool)

    for p in pools:
        if (minr - 1, minc - 1) not in p:
            print('part1:', len(p) + len(lagoon))

    # assert a1 == 0
    # assert a2 == 0


if __name__ == '__main__':
    main()
