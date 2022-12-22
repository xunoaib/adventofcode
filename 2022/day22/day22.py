#!/usr/bin/env python3
import re
import sys

# please... dont read this

WALL = '#'
EMPTY = '.'
OOB = ' '

R, D, L, U = range(4)

offsets = {
    U: (-1, 0),
    R: (0, 1),
    D: (1, 0),
    L: (0, -1),
}

def add(p1, p2):
    return tuple(a + b for a,b in zip(p1, p2))

def sub(p1, p2):
    return tuple(a - b for a,b in zip(p1, p2))

def get_nextpos_pt1(board, src, direction):
    offset = offsets[direction]
    nextpos = add(src, offset)

    if nextpos in board:
        return nextpos, direction

    while src in board:
        src = sub(src, offset)
    return add(src, offset), direction

def get_region(pos, size=50):
    return pos[0] // size, pos[1] // size

def handle_edge_wrapping(pos, direction):
    r,c = pos
    d = direction
    q = get_region(pos)

    if q == (0,1):
        if d == L:
            p = (149 - r, 0)
            d = R
        elif d == U:
            p = (150 + (c - 50), 0)
            d = R

    elif q == (0,2):
        if d == U:
            p = (199, c - 100)
            d = U
        elif d == R:
            p = (149 - r, 99)
            d = L
        elif d == D:
            p = (50 + (c - 100), 99)
            d = L

    elif q == (1,1):
        if d == L:
            p = (100, r - 50)
            d = D
        elif d == R:
            p = (49, 100 + (r - 50))
            d = U

    elif q == (2,1):
        if d == R:
            p = (149 - r, 149)
            d = L
        elif d == D:
            p = (150 + (c - 50), 49)
            d = L

    elif q == (2,0):
        if d == U:
            p = (50 + c, 50)
            d = R
        elif d == L:
            p = (149 - r, 50)
            d = R

    elif q == (3,0):
        if d == L:
            p = (0, 50 + (r - 150))
            d = D
        elif d == D:
            p = (0, 100 + (c - 0))
            d = D
        elif d == R:
            p = (149, 50 + (r - 150))
            d = U

    return p, d

def get_nextpos_pt2(board, p1, d1):
    p2 = add(p1, offsets[d1])

    if board.get(p2, OOB) != OOB:
        return p2, d1

    # ensure warps are correct in the opposite direction
    # if do_assert:
    #     revdir = (d2 + 2) % 4
    #     p3, d3 = get_nextpos_pt2(board, p2, revdir, do_assert=False)
    #     d3 = (d3 + 2) % 4
    #     assert p1 == p3
    #     assert d1 == d3

    return handle_edge_wrapping(p1, d1)

def solve(board, commands, get_nextpos):
    direction = R
    pos = min(board)

    for cmd in commands:
        if cmd == 'L':
            direction -= 1
            direction %= 4
        elif cmd == 'R':
            direction += 1
            direction %= 4
        else:
            for n in range(int(cmd)):
                nextpos, nextdir = get_nextpos(board, pos, direction)
                if board.get(nextpos) != EMPTY:
                    break
                pos = nextpos
                direction = nextdir

    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + direction

def main():
    lines = sys.stdin.read().rstrip().split('\n')

    commands = re.sub(r'([LR])', r' \1 ', lines[-1]).split(' ')
    lines.pop()
    lines.pop()

    board = {}
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch != OOB:
                board[(r,c)] = ch

    ans1 = solve(board, commands, get_nextpos_pt1)
    ans2 = solve(board, commands, get_nextpos_pt2)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 11464
    assert ans2 == 197122

if __name__ == '__main__':
    main()
