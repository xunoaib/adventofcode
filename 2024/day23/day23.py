#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import combinations

lines = sys.stdin.read().strip().split('\n')

g = defaultdict(set)

for line in lines:
    a,b = line.split('-')
    g[a].add(b)
    g[b].add(a)

def part1():

    ans = 0
    for p in combinations(g, r=3):
        if not any(c.startswith('t') for c in p):
            continue

        a,b,c = p
        sa = {a} | g[a]
        sb = {b} | g[b]
        sc = {c} | g[c]

        if set(p).issubset(sa & sb & sc):
            ans += 1
    return ans

results = set()

def all_shared(nodes):
    return all(set(nodes).issubset(g[n]) for n in nodes)

def find_pools(c, seq=tuple()):
    if not seq:
        seq = (c,)

    for n in g[c]:
        if n <= c: # avoid exploring the same route twice
            continue
        newseq = seq + (n,)
        if all_shared(newseq):
            results.add(tuple(sorted(newseq)))
            find_pools(n, newseq)

def part2():
    for c in g:
        g[c].add(c)

    for c in g:
        find_pools(c)

    ans = sorted(max(results, key=len))
    return ','.join(ans)


# a1 = part1()
# print('part1:', a1)

a2 = part2()
print('part2:', a2)

# assert a1 == 1062
assert a2 == 'bz,cs,fx,ms,oz,po,sy,uh,uv,vw,xu,zj,zm'
