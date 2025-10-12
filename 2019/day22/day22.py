import sys

lines = sys.stdin.read().strip().splitlines()
cards: list[int] = list(range(10007))
cards: list[int] = list(range(10))

for line in lines:

    if line == 'deal into new stack':
        cards = cards[::-1]
    elif line.startswith('cut'):
        n = int(line.split()[-1])
        cards = cards[n:] + cards[:n]
    elif line.startswith('deal with increment'):
        n = int(line.split()[-1])
        new_cards: list[int | None] = [None] * len(cards)
        src = tar = 0
        while cards:
            src = (src + n) % len(cards)
            new_cards[tar] = cards.pop(0)
            tar = (tar + n) % len(new_cards)
        cards = new_cards

print(cards)
