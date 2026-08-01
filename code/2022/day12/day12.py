#!/usr/bin/env python3
import sys
from collections import defaultdict

def find_path(edges, start, goal):
    g = {start: 0}
    q = [(0, start)]
    while q:
        cost, pos = q.pop(0)
        for tar in edges[pos]:
            if tar not in g:
                g[tar] = cost + 1
                q.append((cost + 1, tar))
    return g.get(goal, sys.maxsize)

def create_graph(heights):
    edges = defaultdict(list)
    for (r,c), height1 in heights.items():
        for roff, coff in [(1,0), (0,1), (-1,0), (0,-1)]:
            nr = r + roff
            nc = c + coff
            height2 = heights.get((nr, nc))
            if height2 is not None:
                if height2 - height1 <= 1:
                    edges[(r,c)].append((nr,nc))
    return edges

def main():
    lines = sys.stdin.read().strip().split('\n')

    heights = {}
    start = goal = None
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == 'S':
                start = (r,c)
                ch = 'a'
            elif ch == 'E':
                goal = (r,c)
                ch = 'z'
            heights[(r,c)] = ord(ch) - ord('a')

    graph = create_graph(heights)

    ans1 = find_path(graph, start, goal)
    print('part1:', ans1)

    starts = [pos for pos, height in heights.items() if height == 0]
    ans2 = min(find_path(graph, s, goal) for s in starts)
    print('part2:', ans2)

    assert ans1 == 449
    assert ans2 == 443

if __name__ == '__main__':
    main()
