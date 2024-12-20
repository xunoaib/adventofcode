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
def cheat_neighbors(r, c):
    neighbors = set()
    for n in neighbors4(r, c):
        neighbors.add(n)
        for p in neighbors4(*n):
            neighbors.add(p)
    return neighbors

@cache
def cheat_neighbors_length(r, c, length=20):
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

def print_grid(path):
    rows = 1 + max(r for r,c in grid)
    cols = 1 + max(c for r,c in grid)
    for r in range(rows):
        for c in range(cols):
            ch = '\033[91mX\033[0m' if (r,c) in path else grid[r,c]
            print(ch, end='')
        print()

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

a1 = a2 = 0

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

def part1():
    savings = {}
    for src in path:
        for tar in cheat_neighbors_length(*src, 2):
            if tar in track and tar != src:
                dist = abs(src[0]-tar[0]) + abs(src[1]-tar[1])
                savings[src,tar] = fastest_times[src] - fastest_times[tar] - dist

    counts = Counter(savings.values())

    a1 = 0
    for t, freq in sorted(counts.items()):
        if t <= 0:
            continue
        print(f'There are {freq} cheats that save {t} picoseconds.')
        if t >= 100:
            a1 += freq

    # print(fastest_times[start])
    # print(fastest_times[end])

    print('part1:', a1)

def part2():

    savings = {}
    for src in path:
        for tar in cheat_neighbors_length(*src, 20):
            if tar in track and tar != src:
                dist = abs(src[0]-tar[0]) + abs(src[1]-tar[1])
                saved_old = savings.get((src,tar), 0)
                saved_new = fastest_times[src] - fastest_times[tar] - dist
                savings[src,tar] = max(saved_new, saved_old)

    counts = Counter(savings.values())

    a2 = 0
    for t, freq in sorted(counts.items()):
        if t >= 50:
            print(f'There are {freq} cheats that save {t} picoseconds.')
        if t >= 100:
            a2 += freq

    print('part2:', a2)

part1()
part2()
