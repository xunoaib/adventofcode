#!/usr/bin/env python3
import sys
import string
from heapq import heappop, heappush
from collections import defaultdict

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)
CHDIRS = {'>': R, 'v': D}


def alphadict(s):
    return {
        n: string.ascii_letters[i % len(string.ascii_letters)]
        for i, n in enumerate(s)
    }


def neighbors(r, c):
    for roff, coff in DIRS:
        if not (roff == coff == 0):
            yield r + roff, c + coff


def intersections(grid):
    nodes = set()
    for (r, c), ch in grid.items():
        if ch == '#':
            continue
        adjtiles = [grid.get(pos, '#') for pos in neighbors(r, c)]
        numopen = sum(1 for ch in adjtiles if ch != '#')
        if numopen >= 3:
            nodes.add((r, c))
    return nodes | {get_start(grid), get_end(grid)}


def get_start(grid):
    minr = min(r for r, c in grid)
    return [p for p, ch in grid.items() if p[0] == minr and ch == '.'][0]


def get_end(grid):
    maxr = max(r for r, c in grid)
    return [p for p, ch in grid.items() if p[0] == maxr and ch == '.'][0]


def build_graph(grid):
    graph = defaultdict(dict)
    start = get_start(grid)
    q = [(start, )]
    visited = {start}  # excludes junctions
    junctions = intersections(grid)
    while q:
        path = q.pop()
        for npos in neighbors(*path[-1]):
            ch = grid.get(npos, '#')
            if ch == '#' or npos in path:
                continue
            if d := CHDIRS.get(ch):
                if npos != (path[-1][0] + d[0], path[-1][1] + d[1]):
                    continue
            npath = path + (npos, )
            if npos in junctions:
                graph[npath[0]][npath[-1]] = npath
                graph[npath[-1]][npath[0]] = npath
                heappush(q, (npos, ))
            elif npos not in visited:
                visited.add(npos)
                heappush(q, npath)
    return graph


def longest(graph, start, goal):
    assert start in graph and goal in graph
    costs = {start: 0}
    cameFrom = {start: None}
    q = [(0, start, {start})]
    while q:
        cost, current, visited = heappop(q)
        for neighbor, path in graph[current].items():
            path = path[1:]
            if set(path) & visited:
                continue
            ncost = cost - len(path)
            if ncost < costs.get(neighbor, sys.maxsize):
                costs[neighbor] = ncost
                cameFrom[neighbor] = current
                q.append((ncost, neighbor, visited | set(path)))
    return abs(costs[goal])


def main():
    lines = sys.stdin.read().strip().split('\n')
    g = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
    }

    graph = build_graph(g)
    start, end = get_start(g), get_end(g)
    a1 = longest(graph, start, end)

    print('part1:', a1)

if __name__ == '__main__':
    main()
