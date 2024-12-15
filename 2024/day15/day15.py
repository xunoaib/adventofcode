#!/usr/bin/env python3

import sys

dirs = {
    '>': (0,1),
    '<': (0,-1),
    '^': (-1,0),
    'v': (1,0),
}

data,moves = sys.stdin.read().strip().split('\n\n')
lines = data.split('\n')
moves = moves.replace('\n', '')

def part1():

    def print_grid():
        maxr = max(r for r,c in walls)
        maxc = max(c for r,c in walls)
        for r in range(maxr+1):
            for c in range(maxc+1):
                p = r,c
                if p == pos:
                    print('@', end='')
                elif p in walls:
                    print('#', end='')
                elif p in boxes:
                    print('O', end='')
                else:
                    print('.', end='')
            print()
        print()

    grid = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
        if ch != '.'
    }

    boxes = {p for p, ch in grid.items() if ch == 'O'}
    walls = {p for p, ch in grid.items() if ch == '#'}
    pos = next(p for p, ch in grid.items() if ch == '@')

    def nextboxpos(cur, direction):
        while cur in boxes:
            cur = cur[0]+direction[0], cur[1]+direction[1]
        if cur in walls:
            return False
        return cur

    def apply(move):
        nonlocal pos
        r, c = pos
        direction = roff, coff = dirs[move]
        npos = r+roff, c+coff
        if npos in walls:
            return
        if npos in boxes:
            # box can be pushed
            if npos2 := nextboxpos(npos, direction):
                boxes.remove(npos)
                boxes.add(npos2)
                pos = npos
            else:
                return
        pos = npos

    for m in moves:
        apply(m)

    return sum(100 * r + c for r,c in boxes)

def part2():

    def print_grid(highlight=None):
        maxr = max(r for r,c in walls)
        maxc = max(c for r,c in walls)
        for r in range(maxr+1):
            for c in range(maxc+1):
                p = r,c
                ch = ident(p)
                if p == pos:
                    ch = f'\033[91m{ch}\033[0m'
                elif highlight and p in highlight:
                    ch = f'\033[93m{ch}\033[0m'
                print(ch, end='')
            print()
        print()

    d = data
    d = d.replace('#','##')
    d = d.replace('O','[]')
    d = d.replace('.','..')
    d = d.replace('@','@.')
    lines = d.split('\n')

    grid = {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
        if ch != '.'
    }

    lboxes = {p for p, ch in grid.items() if ch == '['}
    rboxes = {p for p, ch in grid.items() if ch == ']'}
    walls = {p for p, ch in grid.items() if ch == '#'}
    pos = next(p for p, ch in grid.items() if ch == '@')

    def nextboxpos(cur, direction):
        while cur in boxes:
            cur = cur[0]+direction[0], cur[1]+direction[1]
        if cur in walls:
            return False
        return cur

    def horiz_pushable(cur, direction):
        boxes = set()
        while cur in lboxes | rboxes:
            boxes.add(cur)
            cur = cur[0]+direction[0], cur[1]+direction[1]
        if cur in walls:
            return set()
        return boxes

    def ident(p):
        if p == pos:
            return '@'
        elif p in walls:
            return '#'
        elif p in lboxes:
            return '['
        elif p in rboxes:
            return ']'
        else:
            return '.'

    def vert_pushable(cur, direction):
        '''Performs the initial push check (and initiates the next two if needed)'''

        if cur in walls:
            return None
        if cur in lboxes:
            lpos = cur
            rpos = cur[0], cur[1]+1
        elif cur in rboxes:
            lpos = cur[0], cur[1]-1
            rpos = cur
        else:
            return {cur}

        lspots = vert_pushable_inner(lpos, direction)
        rspots = vert_pushable_inner(rpos, direction)

        if lspots and rspots:
            return {lpos, rpos} | lspots | rspots

        return None

    def vert_pushable_inner(cur, direction):

        if cur in walls:
            return None

        npos = cur[0]+direction[0], cur[1]+direction[1]

        if npos in walls:
            return None  # cant push

        # pushing into another block
        if npos in rboxes:
            r_pos = npos[0], npos[1]
            l_pos = npos[0], npos[1]-1
        elif npos in lboxes:
            r_pos = npos[0], npos[1]+1
            l_pos = npos[0], npos[1]
        else:
            return {cur}  # can push current block into empty space

        lspots = vert_pushable_inner(l_pos, direction)
        rspots = vert_pushable_inner(r_pos, direction)

        if lspots and rspots:
            return lspots | rspots | {cur}

        return None

    def apply(move):
        nonlocal pos, lboxes, rboxes
        direction = roff, coff = dirs[move]
        npos = pos[0]+roff, pos[1]+coff
        if npos in walls:
            return

        if npos in lboxes | rboxes:
            func = horiz_pushable if move in '<>' else vert_pushable
            if spots := func(npos, direction):
                add_lboxes = {(s[0]+direction[0],s[1]+direction[1]) for s in spots if s in lboxes}
                add_rboxes = {(s[0]+direction[0],s[1]+direction[1]) for s in spots if s in rboxes}
                lboxes -= spots
                rboxes -= spots
                lboxes |= add_lboxes
                rboxes |= add_rboxes
            else:
                return  # not pushable
        pos = npos

    for m in moves:
        apply(m)

    return sum(100 * r + c for r,c in lboxes)

a1 = part1()
print('part1:', a1)

a2 = part2()
print('part2:', a2)

assert a1 == 1436690
assert a2 == 1482350
