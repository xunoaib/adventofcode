#!/usr/bin/env python
import sys
import parse
from pprint import pprint
from collections import defaultdict
import math

SIDES = UP, RIGHT, DOWN, LEFT = 0,1,2,3
AXIS_X, AXIS_Y = AXIS_HORIZ, AXIS_VERT = 0,1

OFFSETS = {
    UP:    (-1,0),
    DOWN:  (1,0),
    RIGHT: (0,1),
    LEFT:  (0,-1),
}

class Tile:
    def __init__(self, block):
        lines = block.strip().split('\n')

        self.id = parse.parse('Tile {:d}:', lines[0])[0]
        self.grid = grid = lines[1:]
        self.nodes = []  # placeholder
        self.transform = (0,0,0) # (rotations, flip_x, flip_y)
        self.pos = None
        self.oriented = False

        edges = []  # top, right, bottom, left (clockwise order)
        edges.append(grid[0])
        edges.append(''.join(grid[r][len(grid[r])-1] for r in range(len(grid))))
        edges.append(grid[-1][::-1])
        edges.append(''.join(grid[r][0] for r in range(len(grid)))[::-1])
        self.edges = edges

    def __repr__(self):
        return f'T{self.id}'

    def flipped_edges(self):
        return [edge[::-1] for edge in self.edges]

    def reflect(self, axis):
        ''' Reflects the values of the given axis/side (other sides is swapped) '''
        axis %= 2
        # reverse direction of all edges
        self.edges = [edge[::-1] for edge in self.edges]

        # swap sides
        for lst in (self.nodes, self.edges):
            lst[axis], lst[axis+2] = lst[axis+2], lst[axis]

    def rotate(self, count):
        ''' Rotates the tile a number of times clockwise '''
        count %= 4
        self.edges = self.edges[-count:] + self.edges[:-count]
        self.nodes = self.nodes[-count:] + self.nodes[:-count]

    def locate_edge(self, edge):
        ''' Locates the given edge (flipped or not) and returns its directional
        position relative to this tile (fuzzy match) '''
        edges = self.edges
        if edge not in edges:
            edges = self.flipped_edges()
        if edge in edges:
            return edges.index(edge)
        return None

    def orient(self, target):
        if not target:
            raise ValueError('invalid target')

        if self.oriented:
            print(target, target.nodes)
            raise ValueError(f'{target} tried to reorient {self}')
        self.oriented = True

        # rotate self into place
        tar_idx = target.nodes.index(self)
        src_idx = self.nodes.index(target)
        offset = tar_idx - src_idx + 2
        self.rotate(offset)

        src_idx = self.nodes.index(target)

        # flip axis if needed
        src_edge = self.edges[src_idx]
        tar_edge = target.edges[tar_idx]

        if src_edge == tar_edge:
            self.reflect(src_idx+1)
            src_edge = self.edges[src_idx]

        if src_edge != tar_edge[::-1]:
            raise ValueError('')

        # set current position relative to target
        side = target.nodes.index(self)
        roff, coff = OFFSETS[side]
        tar_row, tar_col = target.pos
        self.pos = tar_row + roff, tar_col + coff

    def orient_subnodes(self, target=None, side=-1):
        ''' Recursively orients subnodes relative to the given node (or the current node if target=None) '''
        if target:
            self.orient(target)
            print('oriented:', self, 'from', target, target.nodes.index(self), self.nodes, side)
        else: # set self as origin
            self.pos = (0,0)
            self.oriented = True

        # orient all connected nodes
        for side, node in enumerate(self.nodes):
            if node and not node.oriented:
                if node.id == 2801:
                    raise ValueError('should never happen', node)
                node.orient_subnodes(self, side)

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

blocks = sys.stdin.read().split('\n\n')
tiles = list(map(Tile, blocks))
# tileids = {tile.id: tile for tile in tiles}

# find matchable edges
edgemap = defaultdict(set)
for tile in tiles:
    for side,edge in enumerate(tile.edges):
        edgemap[edge].add((tile, side))
    for side,edge in enumerate(tile.flipped_edges()):
        edgemap[edge].add((tile, side))

# find borders
bordercount = defaultdict(lambda: 0)
for edge, tlist in edgemap.items():
    if len(tlist) == 1:
        tile, side = next(iter(tlist))
        bordercount[tile] += 1

# find corners
corners = [tile for tile, count in bordercount.items() if count == 4]
product = math.prod(t.id for t in corners)
print('part1:', product)
assert product == 51214443014783

# part 2

def get_locations(node):
    locations = {node: (0,0)}
    frontier = [node]
    while frontier:
        node = frontier.pop(0)
        row, col = locations.get(node)
        # print(row, col, node)
        for side, neighbor in enumerate(node.nodes):
            if not neighbor:
                continue
            if side not in (RIGHT, DOWN):
                continue
            if neighbor in locations:
                continue
            locations[neighbor] = (row+1, col) if side == DOWN else (row, col+1)
            frontier.append(neighbor)
    return locations

class TileSet:
    def __init__(self, tiles):
        self.tiles = tiles
        self.create_edgemap()
        self.link_neighbors_all()

    def create_edgemap(self):
        ''' Associates edges with tiles that have them (fuzzy match).'''
        edgemap = defaultdict(set)
        for tile in tiles:
            for edge in tile.edges:
                edgemap[edge].add(tile)
                edgemap[edge[::-1]].add(tile)
        self.edgemap = edgemap

    def link_neighbors_all(self):
        '''Creates links between nodes based on matching edges (fuzzy match)'''
        for tile in self.tiles:
            tile.nodes = self.link_neighbors(tile)

    def link_neighbors(self, source):
        '''Returns a list of neighboring nodes for each direction based on edge strings'''
        nodes = []
        for edge in source.edges:
            matches = self.edgemap[edge]
            if len(matches) >= 2:
                node = [n for n in matches if n != source][0] # find other node
            else:
                node = None
            nodes.append(node)
        return nodes

# rename ids
ids = {}
for line in open('ids'):
    old, new = line.strip().split(': ')
    ids[int(old)] = new

for tile in tiles:
    tile.id = ids[tile.id]

# start from upper left corner
corner = corners[0]
ts = TileSet(tiles)

# orient upper left corner
corner.rotate(2)

def debug(node):
    if node:
        print(node, f'{str(node.nodes):<27}', node.edges)

corner.orient_subnodes()

# debug(corner)
# for n in corner.nodes:
#     debug(n)

locs = {tile.pos: tile for tile in tiles}
pprint(locs)

# for tile in tiles:
#     print(tile, tile.pos)

# print(node, node.nodes)
# for node in node.nodes:
#     if node:
#         print(node, node.nodes)

# for row in range(12):
#     for col in range(12):
#         corner = locs.get((row,col))
#         print(corner, end=' ')
#     print('')

# node = tileids[1319]
# node = tileids[3659]
# print(node, node.nodes)
# for n in node.nodes:
#     if n:
#         print(n, n.nodes)

# print(len(nodelocs))
