#!/usr/bin/env python
import sys
import parse
from collections import defaultdict
import math

# notes:
# - the same edge does not appear on more than two tiles
# - there are no symmetric edges

# part 1 - corner tiles are those with 2 unmatched edges (those that dont appear in any other tile).
# these can be found without solving the entire puzzle.

UP, RIGHT, DOWN, LEFT = 0,1,2,3

OFFSETS = {
    UP:    (-1,0),
    DOWN:  (1,0),
    RIGHT: (0,1),
    LEFT:  (0,-1),
}

sea_monster_str = '''
                  #
#    ##    ##    ###
 #  #  #  #  #  #'''.strip('\n')

class Tile:
    def __init__(self, block):
        lines = block.strip().split('\n')

        self.id = parse.parse('Tile {:d}:', lines[0])[0]
        self.grid = grid = lines[1:]
        self.nodes = []  # placeholder
        self.pos = None
        self.oriented = False

        self.transform = [False,False,0] # (flip_y, flip_x, rotations)

        edges = []  # top, right, bottom, left (clockwise order)
        edges.append(grid[0])
        edges.append(''.join(grid[r][len(grid[r])-1] for r in range(len(grid))))
        edges.append(grid[-1][::-1])
        edges.append(''.join(grid[r][0] for r in range(len(grid)))[::-1])
        self.edges = edges

    def __repr__(self):
        return f'T{self.id}'

    def reflect(self, axis):
        ''' Reflects the values of the given axis/side (other sides is swapped) '''
        axis %= 2
        # reverse direction of all edges
        self.edges = [edge[::-1] for edge in self.edges]

        # swap sides
        for lst in (self.nodes, self.edges):
            lst[axis], lst[axis+2] = lst[axis+2], lst[axis]

        # flipped axis varies depending on current number of rotations
        axis = (axis + self.transform[2]) % 2
        self.transform[axis] = not self.transform[axis]

    def rotate(self, count):
        ''' Rotates the tile a number of times clockwise '''
        count %= 4
        self.edges = self.edges[-count:] + self.edges[:-count]
        self.nodes = self.nodes[-count:] + self.nodes[:-count]
        self.transform[2] = (self.transform[2] + count) % 4

    def locate_edge(self, edge):
        ''' Locates the given edge (flipped or not) and returns its directional
        position relative to this tile (fuzzy match) '''
        edges = self.edges
        if edge not in edges:
            edges = [edge[::-1] for edge in self.edges]
        if edge in edges:
            return edges.index(edge)
        return None

    def orient(self, target):
        if not target:
            raise ValueError('invalid target')

        if self.oriented:
            raise ValueError(f'{target} tried to reorient {self}')

        # rotate self into place
        tar_idx = target.nodes.index(self)
        src_idx = self.nodes.index(target)
        offset = tar_idx - src_idx + 2
        self.rotate(offset)

        src_idx = self.nodes.index(target)

        # flip axis if necessary
        src_edge = self.edges[src_idx]
        tar_edge = target.edges[tar_idx]

        # matching edges are always the reverse of each other
        if src_edge == tar_edge:
            self.reflect(src_idx+1)
            src_edge = self.edges[src_idx]

        if src_edge != tar_edge[::-1]:
            raise ValueError('matching edge was reflected incorrectly')

        # set current position relative to the target
        side = target.nodes.index(self)
        roff, coff = OFFSETS[side]
        tar_row, tar_col = target.pos
        self.pos = tar_row + roff, tar_col + coff

        # avoid marking this tile complete if their shared edge is symmetrical (has ambiguous orientation)
        # this allows another tile to eventually orient it
        if src_edge == tar_edge:
            print('ambiguous', self, target)
            return False
        else:
            self.oriented = True
            return True

    def orient_subnodes(self, target=None, side=-1):
        ''' Recursively orients subnodes relative to the given node (or the current node if target=None) '''
        if target:
            # avoid orienting other nodes if the current node is ambiguous
            if not self.orient(target):
                return
        else: # set self as origin
            self.pos = (0,0)
            self.oriented = True

        # orient all connected nodes
        for side, node in enumerate(self.nodes):
            if node and not node.oriented:
                node.orient_subnodes(self, side)

    def transformed_grid(self):
        '''Returns current grid with transformations applied'''
        lines = self.grid
        flipped_y, flipped_x, rotations = self.transform

        if flipped_y:
            lines = lines[::-1]
        if flipped_x:
            lines = [line[::-1] for line in lines]

        for i in range(rotations):
            lines = list(map("".join, zip(*reversed(lines))))

        return lines

    def cropped_grid(self):
        '''Returns current transformed grid with borders removed'''
        lines = self.transformed_grid()
        return [line[1:-1] for line in lines[1:-1]]

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

class TileSet:
    def __init__(self, tiles, num_rows, num_cols):
        self.tiles = tiles
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.create_edgemap()
        self.link_neighbors_all()

    def create_edgemap(self):
        ''' Associates edges with tiles that have them (fuzzy match).'''
        edgemap = defaultdict(set)
        for tile in self.tiles:
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
            if len(matches) not in (0,1,2):
                err = ' '.join(map(str, (source, edge, matches)))
                raise Exception(err)
            if len(matches) == 2:
                node = [n for n in matches if n != source][0] # find other node
            else:
                node = None
            nodes.append(node)
        return nodes

    def grid_tiles(self):
        '''Returns a 12x12 grid of tiles'''
        locs = {tile.pos: tile for tile in self.tiles}
        grid = []
        for row in range(self.num_rows):
            grid.append([])
            for col in range(self.num_cols):
                grid[-1].append(locs[row,col])
        return grid

    def whole_grid(self, borders=False):
        '''Returns the tileset all tile borders cropped as a list of strings'''
        grid = ts.grid_tiles()
        dim = 10 if borders else 8
        lines = ['' for _ in range(dim*self.num_rows)]
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                tile = grid[row][col]
                subgrid = tile.transformed_grid() if borders else tile.cropped_grid()
                for i,line in enumerate(subgrid):
                    lines[row*dim + i] += line
        return lines

def check_links(node):
    ''' Recursively check connected nodes and borders for errors '''
    visited = {node}
    frontier = [node]
    while frontier:
        node = frontier.pop(0)
        # print(node, node.nodes, node.edges)

        # check all edges
        for side,(neighbor,edge1) in enumerate(zip(node.nodes, node.edges)):
            if not neighbor or neighbor in visited:
                continue

            visited.add(neighbor)
            frontier.append(neighbor)

            n_idx = (side + 2) % 4
            edge2, node2 = neighbor.edges[n_idx], neighbor.nodes[n_idx]
            if node2 != node or edge2 == edge1:
                print(neighbor, 'error')
                print(neighbor, neighbor.nodes, neighbor.edges)
                print(node, node.nodes, node.edges)
                print('')
            assert node2 == node and edge2 == edge1[::-1]

def sea_monster_set():
    ''' Returns a list of row/col offsets to check for a sea monster '''
    # row/col offsets for sea monster body
    sea_monster = []
    for r,line in enumerate(sea_monster_str.split('\n')):
        for c,ch in enumerate(line):
            if ch == '#':
                sea_monster.append((r,c))
    return sea_monster

def monster_match(grid, row, col, body):
    ''' Searches for sea monster body at the given location. Returns the set of matching coordinates if found'''
    matches = set()
    for roff,coff in body:
        nr, nc = row+roff, col+coff
        if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[nr]):
            return False
        if grid[nr][nc] != '#':
            return False
        matches.add((nr,nc))
    return matches

def find_monsters(grid):
    ''' Finds the set of all points containing sea monsters '''
    body = sea_monster_set()
    matches = set()
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if cells := monster_match(grid, r, c, body):
                matches |= cells
    return matches

# part 1
blocks = sys.stdin.read().split('\n\n')
tiles = list(map(Tile, blocks))
tileids = {tile.id: tile for tile in tiles}

# find matchable edges
edgemap = defaultdict(set)
for tile in tiles:
    for side,edge in enumerate(tile.edges):
        edgemap[edge].add((tile, side))
        edgemap[edge[::-1]].add((tile, side))

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
dim = int(math.sqrt(len(tiles)))  # grid must be square
ts = TileSet(tiles, dim, dim)

corner = corners[0]  # designate upper left corner

# orient corner (specific to input)
if dim == 3:
    corner.rotate(-3) # sample puzzle
else:
    corner.rotate(2) # my puzzle

corner.orient_subnodes()  # orient all nodes relative to the corner
ts.check_links(corner)    # check for errors

gg = ts.whole_grid()

# reorient final grid (specific to input)
if dim == 3:
    gg = gg[::-1]
    gg = list(map("".join, zip(*reversed(gg))))
else:
    gg = list(map("".join, zip(*reversed(gg))))
    gg = list(map("".join, zip(*reversed(gg))))
    gg = list(map("".join, zip(*reversed(gg))))
    gg = gg[::-1]

# find all coordinates used by monsters
matches = find_monsters(gg)

numhashes = ''.join(gg).count('#')
total = numhashes - len(matches)
print('part2:', total)
assert matches
assert total == 2065

# draw sea monsters
newg = [list(line) for line in gg]
for r,c in matches:
    newg[r][c] = 'O'

# print('\n'.join(gg))
# print('\n'.join(''.join(row) for row in newg))
