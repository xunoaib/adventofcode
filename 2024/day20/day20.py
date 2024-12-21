#!/usr/bin/env python3

import sys
from collections import Counter
from functools import cache
from heapq import heappop, heappush

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


@cache
def cheat_neighbors(r, c, length=20):
    neighbors = {(r,c)}
    q = [(length, (r,c))]
    while q:
        l, p = q.pop(0)
        if l <= 0:
            continue
        for n in neighbors4(*p):
            if n not in neighbors:
                neighbors.add(n)
                q.append((l-1, n))
    return neighbors

lines = sys.stdin.read().strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

walls = {p for p, ch in grid.items() if ch == '#'}
start = next(p for p, ch in grid.items() if ch == 'S')
end = next(p for p, ch in grid.items() if ch == 'E')
track = {p for p, ch in grid.items() if ch != '#'}

grid[start] = '.'
grid[end] = '.'

def shortest_nocheat():
    q = [(0, end)]
    children = {}
    costs = {end: 0}

    while q:
        cost, p = heappop(q)
        for n in neighbors4(*p):
            if n in track and n not in costs:
                children[n] = p
                costs[n] = cost + 1
                heappush(q, (cost + 1, n))

    assert len(costs) == len(track)
    return costs, children

fastest_times, all_children = shortest_nocheat()
fastest_time = fastest_times[start]

path = [start]
p = start
while p := all_children.get(p):
    path.append(p)

def solve(length):
    savings = {}
    for src in path:
        for tar in cheat_neighbors(*src, length):
            if tar in track and tar != src:
                dist = abs(src[0]-tar[0]) + abs(src[1]-tar[1])
                savings[src,tar] = fastest_times[src] - fastest_times[tar] - dist

    counts = Counter(savings.values())
    return sum(freq for t, freq in counts.items() if t >= 100)


a1 = solve(2)
print('part1:', a1)

a2 = solve(20)
print('part2:', a2)

assert a1 == 1372
assert a2 == 979014
