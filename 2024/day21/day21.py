#!/usr/bin/env python3
import sys
from itertools import pairwise


class MyException(Exception): ...

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
    def __init__(self, grid, pos, child: 'Keypad | None', name=None):
        self.grid = grid
        self.pos = pos
        self.child = child
        self.name = name

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

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
            if self.child.pos not in self.child.grid:
                print()
                raise MyException(f'Out of bounds! {button} {self.child.pos} {self}')
        elif button == 'A':
            return self.child.push()
        return ''

    def chain(self):
        ret = [(self.pos, self.grid[self.pos])]
        if self.child:
            ret += self.child.chain()
        return ret

def print_kp(keypad: Keypad):
    maxr = max(r for r,c in keypad.grid)
    maxc = max(c for r,c in keypad.grid)
    rows = ['+---+---+---+']
    for r in range(maxr+1):
        cols = []
        for c in range(maxc+1):
            ch = (' ' + keypad.grid.get((r,c), ' ') + ' ')
            if (r,c) == keypad.pos:
                ch = f'\033[91;1m[{ch.strip()}]\033[0m'
            cols.append(ch)
        rows.append('|' + '|'.join(cols) + '|')
        rows.append('+---+---+---+')

    print('\n'.join(rows))

def print_kp_recursive(k: Keypad):
    if k.child:
        print_kp_recursive(k.child)
    print_kp(k)
    print()

class NumericKeypad(Keypad):
    def __init__(self, child=None, name=None):
        super().__init__(numeric_grid, numeric_start, child, name)

class DirectionalKeypad(Keypad):
    def __init__(self, child=None, name=None):
        super().__init__(directional_grid, directional_start, child, name)

def find_ch(grid, ch):
    return next(p for p, c in grid.items() if c == ch)

def dist_to(grid, src_ch, tar_ch):
    src = find_ch(grid, src_ch)
    tar = find_ch(grid, tar_ch)
    return sub(src, tar)

def Setup():
    kp_num = NumericKeypad(name=3)
    kp_dir1 = DirectionalKeypad(kp_num, 2)
    kp_dir2 = DirectionalKeypad(kp_dir1, 1)
    kp_dir3 = DirectionalKeypad(kp_dir2, 0)
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
        assert actual == expected

DIST_FROM_A = { '<': 3, 'v': 2, '^': 1, '>': 1, 'A': 0}

def find_dist(grid, src, tar, must_travel=False):
    roff, coff = dist_to(grid, src, tar)

    if roff == coff == 0:
        vert_ch = horiz_ch = 'A'
    else:
        vert_ch = '^' if roff < 0 else 'v'
        horiz_ch = '<' if coff < 0 else '>'

    # swap order to avoid going out of bounds
    seq = abs(roff) * vert_ch + abs(coff) * horiz_ch
    if find_ch(grid, src)[1] == 0:
        seq = seq[::-1]
    seq += 'A'

    return (roff, coff), seq

def find_dists(grid, code, must_travel=False):
    totseq = ''
    for src, tar in pairwise('A'+code):
        (roff, coff), seq = find_dist(grid, src, tar, must_travel)
        totseq += seq
    return totseq

def find_ndists(code, must_travel=False):
    return find_dists(ngrid, code, must_travel)

def find_ddists(code, must_travel=False):
    return find_dists(dgrid, code, must_travel)

def simulate(seq):
    k = Setup()
    s = ''
    for i, c in enumerate(seq):
        print(c, s)
        s += k.push_char(c)

    print(s)

def run(code):
    keys1 = find_ndists(code, True)
    keys2 = find_ddists(keys1, True)
    keys3 = find_ddists(keys2, False)
    return keys3

k = Setup()
print_kp_recursive(k)
exit(0)

codes = sys.stdin.read().strip().split('\n')
a1 = 0
for code in codes:
    seq = run(code)
    print(code, len(seq), seq)
    a1 += len(seq) * int(code[:3])

print('part1:', a1)
