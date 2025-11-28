import sys

import networkx as nx

lines = sys.stdin.read().strip().splitlines()

pairs = set()

for line in lines:
    l, rg = line.split(' <-> ')
    pairs |= {(l, r) for r in rg.split(', ')}

G = nx.Graph()
G.add_edges_from(pairs)

for p in nx.connected_components(G):
    if '0' in p:
        print('part1:', len(p))
