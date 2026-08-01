#!/usr/bin/env python3
from itertools import product
from functools import cache
import sys


def part1(p1, p2):
    die, idx = 1, 0
    ps = [p1, p2]
    scores = [0, 0]
    while max(scores) < 1000:
        roll = 3 * die + 3
        ps[idx] = (ps[idx] - 1 + roll) % 10 + 1
        scores[idx] += ps[idx]
        idx = (idx + 1) % 2
        die += 3
    return min(scores) * (die - 1)


def move(turn, pos1, pos2, score1, score2, roll):
    ps = [pos1, pos2]
    scores = [score1, score2]
    ps[turn] = (ps[turn] - 1 + roll) % 10 + 1
    scores[turn] += ps[turn]
    turn = (turn + 1) % 2
    return turn, *ps, *scores


@cache
def winner(turn, pos1, pos2, score1, score2):
    scores = [score1, score2]
    if max(scores) >= 21:
        return [int(s >= 21) for s in scores]
    sums = [0, 0]
    for roll in product((1, 2, 3), repeat=3):
        res = move(turn, pos1, pos2, score1, score2, sum(roll))
        w1, w2 = winner(*res)
        sums[0] += w1
        sums[1] += w2
    return sums


def main():
    p1, p2 = map(int, (line.rsplit(' ')[-1] for line in sys.stdin))

    ans1 = part1(p1, p2)
    print('part1:', ans1)

    ans2 = max(winner(0, p1, p2, 0, 0))
    print('part2:', ans2)

    assert ans1 == 998088
    assert ans2 == 306621346123766


if __name__ == '__main__':
    main()
