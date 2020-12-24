#!/usr/bin/env python
import sys
import copy

decks_orig = [list(map(int, line.split('\n')[1:])) for line in sys.stdin.read().strip().split('\n\n')]

def play_round1(decks):
    c0, c1 = decks[0].pop(0), decks[1].pop(0)
    deck_idx = int(c1 > c0)
    decks[deck_idx] += sorted([c0, c1], reverse=True)
    return len(decks[int(not deck_idx)])

def get_score(deck):
    score = 0
    for i,card in enumerate(deck[::-1], 1):
        score += card * i
    return score

def tuplize(decks):
    return tuple(map(tuple, decks))

def play_round2(decks):
    '''Play one round. Recurses into a subgame to determine the winner if necessary'''
    card0 = decks[0].pop(0)
    card1 = decks[1].pop(0)

    # not enough cards for subgame. compare card values
    if card0 > len(decks[0]) or card1 > len(decks[1]):
        winner = int(card1 > card0)
    else:
        deck0 = decks[0][:card0].copy()
        deck1 = decks[1][:card1].copy()
        winner = play_game2([deck0, deck1])

    # add winner's card to deck before loser
    if winner:
        card0, card1 = card1, card0

    decks[winner] += [card0, card1]
    return winner

def play_game2(decks):
    '''Play rounds until a player is out of cards'''
    history = {tuplize(decks)}
    while True:
        winner = play_round2(decks)

        # out of cards
        if len(decks[winner ^ 1]) == 0:
            return winner

        # check for repeated decks
        decktuple = tuplize(decks)
        if decktuple in history:
            return 0
        history.add(decktuple)

decks = copy.deepcopy(decks_orig)
while play_round1(decks): pass
score = get_score(decks[0] or decks[1])
print('part1:', score)

decks = copy.deepcopy(decks_orig)
winner = play_game2(decks)
print('part2:', get_score(decks[winner]))
