#!/usr/bin/env python3

import sys
from collections import defaultdict


def find_connections(c, seq):
    for n in g[c]:
        if n > c:
            newseq = seq + (n,)
            if set(newseq).issubset(g[n]):
                results.add(newseq)
                find_connections(n, newseq)

lines = sys.stdin.read().strip().split('\n')

g = defaultdict(set)

for line in lines:
    a,b = line.split('-')
    g[a] |= {a, b}
    g[b] |= {a, b}

results = set()

for c in g:
    find_connections(c, (c,))

a1 = sum(len(p) == 3 and any(n.startswith('t') for n in p) for p in results)
print('part1:', a1)

a2 = ','.join(max(results, key=len))
print('part2:', a2)

assert a1 == 1062
assert a2 == 'bz,cs,fx,ms,oz,po,sy,uh,uv,vw,xu,zj,zm'
