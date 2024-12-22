#!/usr/bin/env python3
import sys
from functools import partial
from itertools import pairwise, permutations, product


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
        self.history = ''

    def execute_sequence(self, seq):
        for ch in seq:
            self.push_char(ch)

    def tree(self):
        tree = [self]
        cur = self
        while cur := cur.child:
            tree.append(cur)
        return tree

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

    def push_char(self, ch):
        self.pos = pos = next(p for p,c in self.grid.items() if c == ch)
        return self.push_at(pos)

    def push(self):
        return self.push_at(self.pos)

    def push_at(self, pos):
        return self.push_button(self.grid[pos])

    def push_button(self, button):
        self.history += button
        if not self.child:
            return button

        if button in '<>^v':
            self.child.pos = add(self.child.pos, DIR_OFFSETS[button])
            if self.child.pos not in self.child.grid:
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

def find_dist(grid, src, tar):
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

def find_dists(grid, code):
    totseq = ''
    for src, tar in pairwise('A'+code):
        (roff, coff), seq = find_dist(grid, src, tar)
        totseq += seq
    return totseq

def find_ndists(code):
    return find_dists(ngrid, code)

def find_ddists(code):
    return find_dists(dgrid, code)

def simulate(seq):
    k = Setup()
    s = ''
    for i, c in enumerate(seq):
        print(c, s)
        s += k.push_char(c)
    print(s)

def run(code):
    keys1 = find_ndists(code)
    keys2 = find_ddists(keys1)
    keys3 = find_ddists(keys2)
    print(keys1)
    print(code)
    print(keys2)
    print(keys3)
    print()
    exit(0)
    return keys3

def permute_subsequence(seq, find_func):
    options = []
    for g in seq.split('A'):
        options.append([''.join(u) + 'A' for u in set(permutations(g))])

    # best = (sys.maxsize, None)
    # for p in product(*options):
    #     newseq = find_func(''.join(p))[:-1]
    #     best = min(best, (len(newseq), newseq))
    # return best[1]

    seen = set()
    for p in product(*options):
        yield find_func(''.join(p))[:-1]


def run_brute(code):

    best = (sys.maxsize, None)
    for keys1 in permute_subsequence(code, find_ndists):
        for keys2 in permute_subsequence(keys1, find_ddists):
            for keys3 in permute_subsequence(keys2, find_ddists):
                if len(keys3) >= best[0]:
                    continue

                k = Setup()
                try:
                    k.execute_sequence(keys3)
                    assert k.child.child.child.history == code
                    item = (len(keys3), keys3)
                    best = min(best, item)
                except (MyException, AssertionError):
                    continue
    return best[1]

    # print()
    # keys1 = permute_subsequence(code, find_ndists)
    # print(keys1)
    # keys2 = permute_subsequence(keys1, find_ddists)
    # print(keys2)
    # keys3 = permute_subsequence(keys2, find_ddists)
    # return keys3

def stepwise_render(seq):
    k = Setup()
    outputs = [k.push_char(ch) or ' ' for i, ch in enumerate(seq)]
    k = Setup()
    for i, ch in enumerate(seq):
        print(f'{i:>2}', seq[:i] + f'\033[91m[{ch}]\033[0m' + seq[i+1:])
        print('  ', ''.join(f'[{o}]' if i == j else o for j, o in enumerate(outputs)))
        print()
        print_kp_recursive(k)
        k.push_char(ch)

if __name__ == "__main__":

    # k = Setup()
    # k.execute_sequence('v<<A>>^AAAvA^Av<A<AA>>^AvA^AA<Av>A^Av<<A>A^>A<Av>A^Av<A^>A<A>A')
    # for n in k.tree():
    #     print(n.history)
    # exit(0)

    # seqs = [
    #     # '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',    # correct
    #     # 'v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A' # incorrect
    #     '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A', # correct 379A
    #     'v<<A>>^AvA^Av<<A>>^AAv<<A>A^>AA<Av>AA^Av<A^>AA<A>Av<<A>A^>AAA<Av>A^A' # incorrect 379A
    # ]
    # for seq in seqs:
    #     print()
    #     k = Setup()
    #     try:
    #         k.execute_sequence(seq)
    #     except MyException as exc:
    #         print(exc)
    #     for n in k.tree():
    #         print(n.history)
    # exit(0)

    # seq = 'v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A'
    # stepwise_render(seq)
    # exit(0)

    codes = sys.stdin.read().strip().split('\n')
    a1 = 0
    for code in codes:
        seq = run_brute(code)
        print(code, len(seq), seq)
        a1 += len(seq) * int(code[:3])

    print('part1:', a1)
