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

def to_grid(lines):
    return {
        (r, c): ch
        for r, line in enumerate(lines)
        for c, ch in enumerate(line)
        if ch != '.'
    }

def part1():
    grid = to_grid(lines)
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
    d = data
    d = d.replace('#','##')
    d = d.replace('O','[]')
    d = d.replace('.','..')
    d = d.replace('@','@.')
    lines = d.split('\n')
    grid = to_grid(lines)

    lboxes = {p for p, ch in grid.items() if ch == '['}
    rboxes = {p for p, ch in grid.items() if ch == ']'}
    walls = {p for p, ch in grid.items() if ch == '#'}
    pos = next(p for p, ch in grid.items() if ch == '@')

    def horiz_pushable(cur, direction):
        boxes = set()
        while cur in lboxes | rboxes:
            boxes.add(cur)
            cur = cur[0]+direction[0], cur[1]+direction[1]
        if cur in walls:
            return set()
        return boxes

    def vert_pushable(cur, direction):
        def inner(cur):
            npos = cur[0]+direction[0], cur[1]+direction[1]
            if spots := vert_pushable(npos, direction):
                return spots | {cur}
            return None

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

        lspots = inner(lpos)
        rspots = inner(rpos)

        if lspots and rspots:
            return {lpos, rpos} | lspots | rspots

    def apply(move):
        nonlocal pos, lboxes, rboxes
        direction = dirs[move]
        npos = pos[0]+direction[0], pos[1]+direction[1]
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
