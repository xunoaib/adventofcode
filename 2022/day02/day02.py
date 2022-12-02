#!/usr/bin/env python3
import sys

ROCK = 1
PAPER = 2
SCISSORS = 3

LOSE = 0
DRAW = 3
WIN = 6

def outcome(a, b):
    table = {
        (ROCK, ROCK): DRAW,
        (PAPER, PAPER): DRAW,
        (SCISSORS, SCISSORS): DRAW,

        (ROCK, PAPER): LOSE,
        (PAPER, ROCK): WIN,

        (ROCK, SCISSORS): WIN,
        (SCISSORS, ROCK): LOSE,

        (SCISSORS, PAPER): WIN,
        (PAPER, SCISSORS): LOSE,
    }
    return a + table[(a,b)]

def beats(a):
    return {
        ROCK: PAPER,
        PAPER: SCISSORS,
        SCISSORS: ROCK,
    }[a]

def loses_to(a):
    kv = {
        ROCK: PAPER,
        PAPER: SCISSORS,
        SCISSORS: ROCK,
    }
    kv = {v:k for k,v in kv.items()}
    return kv[a]


def main():
    pairs = [line.strip().split(' ') for line in sys.stdin.readlines()]

    score = 0
    for a, b in pairs:
        a = 'ABC'.index(a) + 1
        b = 'XYZ'.index(b) + 1
        score += outcome(b, a)

    print('part1:', score)
    assert score == 15422

    score = 0
    for a, result in pairs:
        a = 'ABC'.index(a) + 1

        if result == 'X':
            b = loses_to(a)
        elif result == 'Y':
            b = a
        elif result == 'Z':
            b = beats(a)

        score += outcome(b, a)

    print('part2:', score)
    assert score == 15422


if __name__ == "__main__":
    main()
