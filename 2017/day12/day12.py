import sys

import networkx as nx

lines = sys.stdin.read().strip().splitlines()

pairs = set()

for line in lines:
    l, rg = line.split(' <-> ')
    pairs |= {(l, r) for r in rg.split(', ')}

G = nx.Graph()
G.add_edges_from(pairs)

groups = list(nx.connected_components(G))

a1 = next(len(p) for p in groups if '0' in p)
a2 = len(groups)

print('part2:', a1)
print('part2:', a2)
