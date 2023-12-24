#!/usr/bin/env python3
import sys
from collections import defaultdict

DIRS = U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)
SLIDE_DIRS = {'>': R, 'v': D}


def neighbors(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


def find_all_junctions(grid):
    junctions = set()
    for pos in grid:
        numpaths = sum(1 for pos in neighbors(*pos) if pos in grid)
        if numpaths >= 3:
            junctions.add(pos)
    return junctions | {min(grid), max(grid)}


def find_reachable_junctions(grid, current):
    found = {}
    visited = {current}
    alljunctions = find_all_junctions(grid)
    q: list[tuple[int, tuple[int, int]]] = [(0, current)]
    while q:
        cost, current = q.pop()
        for neighbor in neighbors(*current):
            if neighbor in visited or neighbor not in grid:
                continue
            if direction := SLIDE_DIRS.get(grid[neighbor]):
                if direction != (neighbor[0] - current[0],
                                 neighbor[1] - current[1]):
                    continue
            visited.add(neighbor)
            if neighbor in alljunctions:
                found[neighbor] = cost + 1
                continue
            q.append((cost + 1, neighbor))
    return found


def build_graph(grid):
    graph = defaultdict(dict)
    for src in find_all_junctions(grid):
        for dst, cost in find_reachable_junctions(grid, src).items():
            graph[src][dst] = cost
    return dict(graph)


class Solver:

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def solve(self, graph):
        self.graph = graph
        self.best = 0
        return self.maximize(self.start, (self.start, ))

    def maximize(self, current, path, cost=0):
        if current == self.goal:
            return cost

        for neighbor, pcost in self.graph[current].items():
            if neighbor not in path:
                self.best = max(
                    self.best,
                    self.maximize(neighbor, path + (neighbor, ), cost + pcost))

        return self.best


def main():
    lines = sys.stdin.read().strip().split('\n')
    grid = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line) if ch != '#'
    }
    grid2 = {pos: '.' for pos in grid}
    start, goal = min(grid), max(grid)

    graph1 = build_graph(grid)
    graph2 = build_graph(grid2)

    s = Solver(start, goal)

    a1 = s.solve(graph1)
    print('part1:', a1)

    a2 = s.solve(graph2)
    print('part2:', a2)

    assert a1 == 2210
    assert a2 == 6522


if __name__ == '__main__':
    main()
