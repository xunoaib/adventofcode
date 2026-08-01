#!/usr/bin/env python3
import sys
from collections import defaultdict
from heapq import heappop, heappush

MAXR = MAXC = None
START = GOAL = None

def next_blizzard_pos(pos, char):
    r,c = pos
    match char:
        case '>':
            c += 1
        case '<':
            c -= 1
        case '^':
            r -= 1
        case 'v':
            r += 1

    if r <= 0:
        r = MAXR - 1
    if c <= 0:
        c = MAXC - 1
    if r >= MAXR:
        r = 1
    if c >= MAXC:
        c = 1
    return r, c

def next_blizzards(blizzards):
    new_blizzards = defaultdict(list)
    for pos, chars in blizzards.items():
        for char in chars:
            newpos = next_blizzard_pos(pos, char)
            new_blizzards[newpos].append(char)
    return new_blizzards

def get_moves(blizzards, pos):
    moves = []
    r, c = pos

    for roff in [-1,0,1]:
        for coff in [-1,0,1]:
            if 0 not in (roff,coff):
                continue
            nr, nc = npos = (r + roff, c + coff)

            if nr in (0, MAXR) and (nr, nc) not in (START, GOAL):
                continue

            if 0 <= nr <= MAXR and 1 <= nc <= MAXC - 1 and npos not in blizzards:
                moves.append(npos)
    return moves

def heuristic(pos, goal):
    return sum(abs(a - b) for a,b in zip(pos, goal))

def solve(blizzards, start, goal):
    history = {-1: blizzards}
    q = [(0, start)]

    gScore = defaultdict(lambda: sys.maxsize)
    gScore[(0, start)] = 0

    # I don't think I'm correctly using fScore here, but it still works
    fScore = defaultdict(lambda: sys.maxsize)
    fScore[(0, start)] = heuristic(start, goal)

    while q:
        current_state = minute, current = heappop(q)

        if current == goal:
            return minute, history[minute - 1]

        if minute not in history:
            history[minute] = next_blizzards(history[minute-1])
        blizzards = history[minute]

        for neighbor in get_moves(blizzards, current):
            neighbor_state = (minute + 1, neighbor)

            tentative_gScore = gScore[current_state] + 1
            if tentative_gScore < gScore[neighbor_state]:
                gScore[neighbor_state] = tentative_gScore
                fScore[neighbor_state] = tentative_gScore + heuristic(neighbor, goal)

            if neighbor_state not in q:
                heappush(q, neighbor_state)

def main():
    global MAXR, MAXC, START, GOAL
    lines = sys.stdin.read().strip().split('\n')

    MAXR = len(lines) - 1
    MAXC = len(lines[0]) - 1

    START = (0, lines[0].index('.'))
    GOAL = (MAXR, lines[-1].index('.'))

    blizzards = defaultdict(list)
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch not in '#.':
                blizzards[(r,c)].append(ch)

    ans1, blizzards = solve(blizzards, START, GOAL)
    print('part1:', ans1)

    GOAL, START = START, GOAL
    t2, blizzards = solve(blizzards, START, GOAL)

    GOAL, START = START, GOAL
    t3, blizzards = solve(blizzards, START, GOAL)

    ans2 = ans1 + t2 + t3
    print('part2:', ans2)

    assert ans1 == 343
    assert ans2 == 960

if __name__ == '__main__':
    main()
