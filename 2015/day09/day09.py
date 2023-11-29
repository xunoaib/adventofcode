#!/usr/bin/env python3
import re
import sys
from collections import defaultdict
from heapq import heappop, heappush


def hamilton(G):
    """Find all Hamiltonian paths and their total costs.
    G: Nested graph of vertices and costs where G[v1][v2] = distance between v1 & v2
    """
    h = [(0, (node,)) for node in G]
    solutions = []
    while h:
        dist, path = heappop(h)
        node = path[-1]

        if len(path) == len(G):
            solutions.append((dist, path))
            continue

        for nextnode, cost in G[node].items():
            if nextnode not in path:
                heappush(h, (dist + cost, path + (nextnode,)))

    return sorted(solutions)

def main():
    lines = sys.stdin.read().strip().split('\n')
    graph = defaultdict(dict)
    for line in lines:
        a, b, dist = re.match('(.*) to (.*) = (.*)', line).groups()
        dist = int(dist)
        graph[a][b] = dist
        graph[b][a] = dist

    paths = hamilton(graph)

    ans1 = paths[0][0]
    print('part1:', ans1)

    ans2 = paths[-1][0]
    print('part2:', ans2)

    assert ans1 == 117
    assert ans2 == 909

if __name__ == '__main__':
    main()
