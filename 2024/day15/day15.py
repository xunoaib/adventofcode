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
            # if box can be pushed
            if npos2 := nextboxpos(npos, direction):
                if npos2 in walls | boxes:
                    return
                boxes.remove(npos)
                boxes.add(npos2)
                pos = npos
            else:
                return
        pos = npos

    for i,m in enumerate(moves):
        apply(m)

    a1 = 0
    for r,c in boxes:
        a1 += 100 * r + c
    return a1

def part2():

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
                elif p in lboxes:
                    print('[', end='')
                elif p in rboxes:
                    print(']', end='')
                else:
                    print('.', end='')
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

    def apply(move):
        nonlocal pos
        r, c = pos
        direction = roff, coff = dirs[move]
        npos = r+roff, c+coff
        if npos in walls:
            return
        if npos in boxes:
            # if box can be pushed
            if npos2 := nextboxpos(npos, direction):
                if npos2 in walls | boxes:
                    return
                boxes.remove(npos)
                boxes.add(npos2)
                pos = npos
            else:
                return
        pos = npos

    for i,m in enumerate(moves):
        apply(m)

    a1 = 0
    for r,c in boxes:
        a1 += 100 * r + c
    return a1

a1 = part1()
a2 = part2()

print('part1:', a1)
print('part2:', a2)

assert a1 == 1436690
# assert a2 == 0
