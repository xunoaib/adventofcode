#!/usr/bin/env python3
import sys
from collections import Counter


def score_part1(cards):
    cardcounts = Counter(cards)
    counts = set(cardcounts.values())

    if 5 in counts:
        return 6
    if 4 in counts:
        return 5
    if {3, 2}.issubset(counts):
        return 4
    if 3 in counts:
        return 3
    if Counter(cardcounts.values())[2] == 2:
        return 2
    if 2 in counts:
        return 1
    return 0


def score_part2(cards, idx=0):
    if idx >= len(cards):
        return score_part1(cards)
    if cards[idx] != 0:
        return score_part2(cards, idx + 1)

    best = 0
    copy = list(cards)
    for val in range(2, 15):
        copy[idx] = val
        best = max(best, score_part2(copy, idx + 1))
    return best


def key_sort_func(hand, score_func):
    return (score_func(hand), ) + tuple(hand)


def solve(lines, cardvals, score_func):
    hands = []
    bids = {}
    for line in lines:
        hand, bid = line.split()
        hand = tuple(cardvals[c] if c in cardvals else int(c) for c in hand)
        hands.append(hand)
        bids[hand] = int(bid)

    ans = 0
    hands.sort(key=lambda h: key_sort_func(h, score_func))
    for rank, hand in enumerate(hands, 1):
        ans += rank * bids[hand]
    return ans


def main():
    lines = sys.stdin.read().strip().split('\n')
    cardvals = dict(zip('TJQKA', range(10, 15)))

    ans1 = solve(lines, cardvals, score_part1)
    print('part1:', ans1)

    cardvals['J'] = 0
    ans2 = solve(lines, cardvals, score_part2)
    print('part2:', ans2)

    assert ans1 == 247961593
    assert ans2 == 248750699


if __name__ == '__main__':
    main()
