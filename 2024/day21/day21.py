#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from itertools import pairwise

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)

DIR_OFFSETS = {
    '>': R,
    '<': L,
    '^': U,
    'v': D,
}

def add(a, b):
    return a[0]+b[0], a[1]+b[1]

def sub(a, b):
    return b[0]-a[0], b[1]-a[1]

numeric_chars = '789\n456\n123\n.0A'
directional_chars = '.^A\n<v>'

ngrid = numeric_grid = {
    (r, c): ch
    for r, line in enumerate(numeric_chars.split('\n'))
    for c, ch in enumerate(line)
    if ch != '.'
}

dgrid = directional_grid = {
    (r, c): ch
    for r, line in enumerate(directional_chars.split('\n'))
    for c, ch in enumerate(line)
    if ch != '.'
}

numeric_start = next(p for p, ch in numeric_grid.items() if ch == 'A')
directional_start = next(p for p, ch in directional_grid.items() if ch == 'A')

def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff

class Keypad:
    def __init__(self, grid, pos, child: 'Keypad | None'):
        self.grid = grid
        self.pos = pos
        self.child = child

    def push_char(self, ch):
        pos = next(p for p,c in self.grid.items() if c == ch)
        return self.push_at(pos)

    def push(self):
        return self.push_at(self.pos)

    def push_at(self, pos):
        return self.push_button(self.grid[pos])

    def push_button(self, button):
        if not self.child:
            return button

        if button in '<>^v':
            self.child.pos = add(self.child.pos, DIR_OFFSETS[button])
            assert self.child.pos in self.child.grid
        elif button == 'A':
            if self.child:
                return self.child.push()
        return ''

    def chain(self):
        ret = [(self.pos, self.grid[self.pos])]
        if self.child:
            ret += self.child.chain()
        return ret

class NumericKeypad(Keypad):
    def __init__(self, child=None):
        super().__init__(numeric_grid, numeric_start, child)

class DirectionalKeypad(Keypad):
    def __init__(self, child=None):
        super().__init__(directional_grid, directional_start, child)

def find_ch(grid, ch):
    return next(p for p, c in grid.items() if c == ch)

def dist_to(grid, src_ch, tar_ch):
    src = find_ch(grid, src_ch)
    tar = find_ch(grid, tar_ch)
    rdiff, cdiff = sub(src, tar)
    return abs(rdiff), abs(cdiff)

def Setup():
    kp_num = NumericKeypad()
    kp_dir1 = DirectionalKeypad(kp_num)
    kp_dir2 = DirectionalKeypad(kp_dir1)
    kp_dir3 = DirectionalKeypad(kp_dir2)
    return kp_dir3

def test():
    seqs = [
        ('029A', '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'),
        ('980A', '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A'),
        ('179A', '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'),
        ('456A', '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A'),
        ('379A', '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'),
    ]
    for expected, seq in seqs:
        k = Setup()
        actual = ''.join(k.push_char(ch) for ch in seq)
        print(actual)
        assert actual == expected

test()

# def dist_to(src, tar):
#     a, b = sub(src, tar)
#     return abs(a) + abs(b)
#
# def pos_of_char(grid, search_ch):
#     return next(p for p, ch in grid.items() if ch == search_ch)
#
# def numeric_dists(code, start_pos):
#     positions = [start_pos] + [pos_of_char(numeric_grid, ch) for ch in code]
#     dists = [dist_to(a, b) for a,b in pairwise(positions)]
#
# codes = sys.stdin.read().strip().split('\n')
#
# for code in codes:
#     print(code)
#
#     numeric_pos = numeric_start
#     dists = numeric_dists(code, numeric_pos)
#
#     exit(0)