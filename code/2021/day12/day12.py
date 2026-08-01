#!/usr/bin/env python3
import sys
from collections import defaultdict, Counter

def part1(graph):
    frontier = [('start', tuple())]
    solutions = set()
    while frontier:
        node, path = frontier.pop()
        if node == 'end':
            solutions.add(path)
            continue

        for next_node in graph[node]:
            if next_node.islower() and next_node in path:
                continue
            newpath = path + (node,)
            frontier.append((next_node, newpath))
    return len(solutions)

def part2(graph):
    frontier = [('start', ('start',))]
    solutions, visited = set(), set()

    while frontier:
        node, path = frontier.pop()
        if node == 'end':
            solutions.add(path)
            continue

        for next_node in graph[node]:
            next_path = path + (next_node,)

            if next_path in visited:
                continue
            visited.add(next_path)

            if next_node == 'start':
                continue

            if next_node.islower():
                if next_path.count(next_node) > 2:
                    continue

                # warning: slow and lazy
                low_counts = Counter(n for n in next_path if n.islower())
                if low_counts[next_node] > 2 or list(low_counts.values()).count(2) > 1:
                    continue
            frontier.append((next_node, next_path))
    return len(solutions)

def main():
    graph = defaultdict(set)
    for line in sys.stdin:
        a, b = line.strip().split('-')
        graph[a].add(b)
        graph[b].add(a)
    graph = dict(graph)

    ans1 = part1(graph)
    print('part1:', ans1)

    ans2 = part2(graph)
    print('part2:', ans2)

    assert ans1 == 4659
    assert ans2 == 148962

if __name__ == '__main__':
    main()
