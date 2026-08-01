#!/usr/bin/env python3
import sys

ROCK = 1
PAPER = 2
SCISSORS = 3

LOSE = 0
DRAW = 3
WIN = 6

# looks up the winning move against another move
winner_against = {
    ROCK: PAPER,
    PAPER: SCISSORS,
    SCISSORS: ROCK,
}

loser_against = {v:k for k,v in winner_against.items()}

def score_outcome(a, b):
    outcomes = {
        (a, loser_against[a]): WIN,
        (a, a): DRAW,
        (a, winner_against[a]): LOSE,
    }
    return a + outcomes[(a,b)]


def main():
    pairs = [line.strip().split(' ') for line in sys.stdin.readlines()]

    score = 0
    for a, b in pairs:
        a = 'ABC'.index(a) + 1
        b = 'XYZ'.index(b) + 1
        score += score_outcome(b, a)

    print('part1:', score)
    assert score == 15422

    score = 0
    for a, b in pairs:
        a = 'ABC'.index(a) + 1

        match b:
            case 'X':
                b = loser_against[a]
            case 'Y':
                b = a
            case 'Z':
                b = winner_against[a]

        score += score_outcome(b, a)

    print('part2:', score)
    assert score == 15442


if __name__ == "__main__":
    main()
