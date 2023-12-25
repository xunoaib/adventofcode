#!/usr/bin/env python3
import re
import sys
from collections import defaultdict


def draw_graph(nodes):
    import networkx as nx
    import matplotlib.pyplot as plt
    g = nx.Graph()
    for node, others in nodes.items():
        for other in others:
            g.add_edge(node, other)

    nx.draw_networkx(g, with_labels=True, font_weight='bold')
    print('done')
    plt.gca()
    plt.axis('off')
    plt.show()


def main():
    lines = sys.stdin.read().strip().split('\n')
    nodes = defaultdict(set)

    for line in lines:
        if m := re.match(r'(.*): (.*)', line):
            lhs, rest = m.groups()
            rest = set(rest.split(' '))
            nodes[lhs] |= rest
            for rhs in rest:
                nodes[rhs].add(lhs)

    def remove(u, v):
        nodes[u].remove(v)
        nodes[v].remove(u)

    def explore(src):
        visited = set()
        q = [src]
        while q:
            current = q.pop()
            for n in nodes[current]:
                if n not in visited:
                    visited.add(n)
                    q.append(n)
        return visited

    # # we can manually identify which three edges must be cut :)
    # draw_graph(nodes)

    remove('tvj', 'cvx')
    remove('nct', 'kdk')
    remove('fsv', 'spx')

    a = explore('cvx')
    b = explore('fsv')

    a1 = len(a) * len(b)
    print('part1:', a1)

    assert a1 == 532891


if __name__ == '__main__':
    main()
